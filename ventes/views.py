from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from dashboard.utils import Utils, RedirectToPreviousMixin

from dashboard.models import ProductModel, Shop
from clients.models import ClientModel
from ventes.models import VenteModel
from ventes.forms import VenteForm

from django.core.exceptions import ValidationError
# Create your views here.


class VenteView(LoginRequiredMixin, CreateView, Utils):

    template_name = 'ventes/vente.html'
    form_class = VenteForm
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
            messages.error(self.request, "Il ne reste que {} object(s) de {}. Donc cette vente ne peut être effectuée".format(
                product.quantity, product.name))
            return redirect(reverse('ventes:ventePage'))
        # elif remaining_qty == 0:
        #     ProductModel.objects.filter(pk=form.instance.produit.pk).delete()
        else:
            product.quantity = remaining_qty
            product.initial_quantity = product.quantity + vente_qty
        # 
        price_vente_minimum = product.price_vente_minimum_ad or product.price_vente_minimum_dv
        if price_vente_minimum < form.instance.price:
                messages.warning(self.request, "Vous êtes entrain de vendre à un prix inférieur. Vous pouvez aller modifier la vente du produit {}".format(product.name))        
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
            
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vente"
        uname = self.request.user.username
        if self.request.user.is_superuser:
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


class VenteUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'ventes/vente_edit.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('ventes:ventePage')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(owner__user__username=self.request.user.username)
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

#Delete Multiple Vente
def multiple_delete_vente(request): 
    if request.method == 'POST':
        vente_ids = request.POST.getlist('id[]')
        for id in vente_ids: 
            vente = VenteModel.objects.get(pk=id)
            vente.delete()
    return redirect('clients:clientPage')

#404 page not found
