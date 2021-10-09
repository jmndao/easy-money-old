from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from dashboard.utils import Utils, RedirectToPreviousMixin

from dashboard.models import ProductModel, Shop
from clients.models import ClientModel
from ventes.forms import VenteForm
from ventes.models import VenteModel


# Create your views here.

def vente_list_view(request):

    u = Utils()

    # Get the connected user
    conn_user = request.user

    # context to render
    context = {}

    # Render the list of all client in context and pks
    context['clients'] = ClientModel.objects.all().order_by('-created_date')[:10]

    # What superuser and simple_user sees are at some 
    # point different that's why their context rendering
    # is also different
    if conn_user.is_superuser:
        context['vente'] = q = VenteModel.objects.order_by(
            '-created_date')
        context["tendance_vente"] = VenteModel.objects.values(
            'produit__name').annotate(freq=Count('produit__name')).order_by("?")
        context['count_item'] = q.count()
        context['revenue'] = sum(
            [p.price_total for p in q if p.price_total != None])
        context["dataset_vente"] = u.chart_vente(
            VenteModel, key='price_total', dt_col_name='created_date')
        context['benefice'] = u.benefice_vente(
            VenteModel, ProductModel)
    else:
        context['vente'] = q = VenteModel.objects.filter(produit__shop__owner__user__username=conn_user.username).order_by(
            '-created_date')
        context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=conn_user.username).values(
            'produit__name').annotate(freq=Count('produit__name')).order_by("?")
        context['count_item'] = q.count()
        context['revenue'] = sum(
            [p.price_total for p in q if p.price_total != None])
        context["dataset_vente"] = u.chart_vente(
            VenteModel, key='price_total', dt_col_name='created_date', uname=conn_user.username, is_superuser=False)
        context['benefice'] = u.benefice_vente(
            VenteModel, ProductModel, is_superuser=False, user=conn_user)

    return render(request, 'ventes/vente.html', context)


def vente_creation_view(request, pk):

    # Get the connected user
    conn_user = request.user

    # Create inline formset for multiple vente
    VenteFormSet = inlineformset_factory(ClientModel,
                                         VenteModel,
                                         form=VenteForm,
                                         extra=5,
                                         max_num=10,
                                         fields=(
                                            'produit', 
                                            'price', 
                                            'acompte', 
                                            'quantity', 
                                            'guarantee', 
                                            'guarantee_period'
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
                if not conn_user.is_superuser:
                    form.instance.shop = Shop.objects.get(
                        owner__user__username=conn_user.username)
                    if form.instance.produit.pk:
                        product = ProductModel.objects.get(pk=form.instance.produit.pk)
                        product.sold = True

                        form.instance.price_total = form.instance.price * form.instance.quantity
                        vente_qty = form.instance.quantity
                        remaining_qty = product.quantity - vente_qty
                        if remaining_qty < 0:
                            messages.error(request, "Il ne reste que {} {}. Donc cette vente ne peut être effectuée".format(
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
                                request, "Attention vous vendez au prix minimum conseillé. Vous pouvez modifier la vente du produit {}".format(product.name))
                        product.save()
                        client = form.instance.client
                        try:
                            not_new_client = ClientModel.objects.get(pk=client.pk)
                        except Exception as e:
                            not_new_client = None
                        if not_new_client:
                            # the client is not new.
                            not_new_client.passage += 1
                            not_new_client.save()
                        else:
                            pass
            formset.save()
            last_vente = VenteModel.objects.all().order_by('-created_date')[0]
            return redirect(reverse('dashboard:invoice', args=(last_vente.pk,)))

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


class VenteDetailView(LoginRequiredMixin, DetailView):

    template_name = 'ventes/vente_detail.html'
    model = VenteModel
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Vente"
        return context


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
