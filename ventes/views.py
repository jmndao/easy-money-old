import datetime
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from dashboard.utils import Utils, RedirectToPreviousMixin

from dashboard.models import ProductModel, Shop
from clients.models import ClientModel
from ventes.forms import VenteForm, VenteFormSingle
from ventes.models import VenteModel

from templated_email import send_templated_mail
from django.conf import settings


# Create your views here.

class VenteView(LoginRequiredMixin, CreateView, Utils):

    template_name = 'ventes/vente.html'
    form_class = VenteFormSingle
    success_url = reverse_lazy('ventes:ventePage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        # check if we choose the right quantities or not?
        ################################################################
        u_user = self.request.user
        if not u_user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=u_user.username)
        product = ProductModel.objects.get(pk=form.instance.produit.pk)
        product.sold = True

        form.instance.price_total = form.instance.price * form.instance.quantity
        vente_qty = form.instance.quantity
        remaining_qty = product.quantity - vente_qty
        if remaining_qty < 0:
            messages.error(self.request, "Il ne reste que {} {}. Donc cette vente ne peut être effectuée".format(
                product.quantity, product.name))
            return redirect(reverse('ventes:ventePage'))
        # elif remaining_qty == 0:
        #     ProductModel.objects.filter(pk=form.instance.produit.pk).delete()
        else:
            product.quantity = remaining_qty
            product.initial_quantity = product.quantity + vente_qty
        #
        price_vente_minimum = product.price_vente_minimum_ad or product.price_vente_minimum_dv
        if form.instance.price < price_vente_minimum:
            messages.warning(
                self.request, "Attention vous vendez au prix minimum conseillé. Vous pouvez modifier la vente du produit {}".format(product.name))
        product.save()
        client = form.instance.client
        client.passage += 1

        ventes = [
            {
                'client': form.instance.client,
                'produit': form.instance.produit,
                'quantity': form.instance.quantity,
                'price': form.instance.price,
                'price_total': form.instance.price_total
            }
        ]

        # Send Invoice to client by email
        if client.email:
            send_templated_mail(
                template_name='invoice',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                context={
                    'ventes': ventes,
                    'total_price': form.instance.price_total
                }
            )
        # This client has been invoiced for today
        client.invoiced = True
        client.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vente"
        uname = self.request.user.username
        if self.request.user.is_superuser:
            context['vs'] = VenteModel.objects.annotate(c_date=TruncDay('created_date')).values(
                'c_date', 'client__fname', 'client__lname', 'client__pk').annotate(c=Count('id'), total=Sum('price_total')).order_by()
            context['vente'] = self.q = VenteModel.objects.order_by(
                '-created_date')
            context["tendance_vente"] = VenteModel.objects.values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
            context['count_item'] = self.q.count()
            context['revenue'] = sum(
                [p.price_total for p in self.q if p.price_total != None])
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date')
            context['benefice'] = self.benefice_vente(
                VenteModel, ProductModel)
        else:
            context['vs'] = VenteModel.objects.filter(
                produit__shop__owner__user__username=uname).annotate(
                    c_date=TruncDay('created_date')).values(
                'c_date', 'client__fname', 'client__lname', 'client__pk').annotate(
                    c=Count('id'), total=Sum('price_total')).order_by()
                    
            context['vente'] = self.q = VenteModel.objects.filter(produit__shop__owner__user__username=uname).order_by(
                '-created_date')
            context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=uname).values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
            context['count_item'] = self.q.count()
            context['revenue'] = sum(
                [p.price_total for p in self.q if p.price_total != None])
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date', uname=uname, is_superuser=False)
            context['benefice'] = self.benefice_vente(
                VenteModel, ProductModel, is_superuser=False, user=self.request.user)

        return context


def multiple_vente_creation_view(request, pk):

    type_de_service, type_de_reglement = 0, ''
    # Get the connected user
    conn_user = request.user

    # Create inline formset for multiple vente
    VenteFormSet = inlineformset_factory(ClientModel,
                                            VenteModel,
                                            form=VenteForm,
                                            extra=10,
                                            can_delete=False,
                                            fields=(
                                                'produit',
                                                'price',
                                                'acompte',
                                                'quantity',
                                                'guarantee',
                                                'guarantee_period',
                                                'type_de_service',
                                                'type_de_reglement',
                                                'price_remise'
                                            )
                                         )
    # Pick the selected client
    client = ClientModel.objects.get(pk=pk)

    formset = VenteFormSet(
        queryset=VenteModel.objects.none(),
        instance=client)

    if request.method == 'POST':
        formset = VenteFormSet(request.POST, instance=client)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if not conn_user.is_superuser:
                        form.instance.shop = Shop.objects.get(
                            owner__user__username=conn_user.username)
                    if form.instance.produit:
                        product = ProductModel.objects.get(
                            pk=form.instance.produit.pk)
                        product.sold = True
                        # Calculating the total price here (Tt = price * Qty)
                        form.instance.price_total = (form.instance.price * form.instance.quantity) - form.instance.price_remise
                        # Calculate the remaining quantity
                        remaining_qty = product.quantity - form.instance.quantity

                        if remaining_qty < 0:
                            messages.error(request, "Il ne reste que {} {}. Donc cette vente ne peut être effectuée".format(
                                product.quantity, product.name))
                            return redirect(reverse('ventes:ventePage'))
                        # elif remaining_qty == 0:
                        #     ProductModel.objects.filter(pk=form.instance.produit.pk).delete()
                        # Update the remaining quantity here
                        else:
                            product.quantity = remaining_qty
                            product.initial_quantity = product.quantity + form.instance.quantity
                        #
                        price_vente_minimum = product.price_vente_minimum_ad or product.price_vente_minimum_dv

                        if form.instance.price < price_vente_minimum:
                            messages.warning(
                                request, "Attention vous vendez au prix minimum conseillé. Vous pouvez modifier la vente du produit {}".format(product.name))
                        product.save()

                        try:
                            client.passage += 1
                            client.save()
                        except Exception as e:
                            pass

                        if form.instance.type_de_service:
                            type_de_service = int(
                                form.instance.type_de_service)
                        if form.instance.type_de_reglement:
                            type_de_reglement = form.instance.type_de_reglement

                        if type_de_service or type_de_reglement:
                            form.instance.type_de_service = type_de_service
                            form.instance.type_de_reglement = type_de_reglement

                        form.save()

            last_vente = VenteModel.objects.all().order_by('-created_date')[0]
            # today = datetime.date.today()

            ventes = VenteModel.objects.filter(client=client,
                                               created_date__day=last_vente.created_date.day
                                               )

            total_price = sum([v.price_total for v in ventes if v.price_total])

            # Send Invoice to client by email
            if client.email:
                send_templated_mail(
                    template_name='invoice',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    context={
                        'ventes': ventes,
                        'total_price': total_price
                    }
                )
            # This client has been invoiced for today
            client.invoiced = True
            client.save()

            return redirect(reverse('dashboard:invoice', args=(client.pk, 
                last_vente.created_date.day, last_vente.created_date.month, last_vente.created_date.year)))

    context = {
        'formset': formset,
        'client': client
    }

    return render(request, 'ventes/facture.html', context)


class VenteUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'ventes/vente_edit.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('ventes:ventePage')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Vente"
        return context


def vente_detail(request, pk, day):

    ventes = VenteModel.objects.filter(
        client__pk=pk, created_date__day=day)
    client = ClientModel.objects.get(pk=pk)

    context = {
        "title": "Detail-Vente",
        "ventes": ventes,
        "client": client,
    }
    return render(request, "ventes/vente_detail.html", context)


class VenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'ventes/vente_delete.html'
    model = VenteModel
    context_object_name = 'vente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Vente"
        return context

# Delete Multiple Vente


def multiple_delete_vente(request):
    if request.method == 'POST':
        vente_ids = request.POST.getlist('id[]')
        for id in vente_ids:
            vente = VenteModel.objects.get(pk=id)
            vente.delete()
    return redirect('clients:clientPage')

# 404 page not found
