from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Count
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import (TemplateView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from dashboard.models import (ProductModel, Shop)

from clients.models import ClientModel
from ventes.models import VenteModel

from dashboard.utils import Utils, RedirectToPreviousMixin
from dashboard.forms import ProductModelForm


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView, Utils):

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['n_shops'] = Shop.objects.all().count()
        if self.request.user.is_superuser:
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date')
            context['dataset_depot'] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='DV', dt_col_name='created_date')
            context["dataset_achat"] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='AD', dt_col_name='created_date')
            context["achat_directs"] = ProductModel.objects.filter(dv_or_ad='AD').order_by(
                '-created_date')
            context["depot_ventes"] = ProductModel.objects.filter(dv_or_ad='DV').order_by(
                '-created_date')
            context["ventes"] = VenteModel.objects.all().order_by(
                '-created_date')
            context["tendance_vente"] = VenteModel.objects.values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
            context["tendance_achat_direct"] = ProductModel.objects.filter(dv_or_ad='AD').values(
                'name').annotate(freq=Count('name')).order_by("?")
            context["tendance_depot_vente"] = ProductModel.objects.filter(dv_or_ad='DV').values(
                'name').annotate(freq=Count('name')).order_by("?")
            context["n_product"] = ProductModel.objects.all().count()
            context["n_client"] = ClientModel.objects.all().count()
            context['benefice_day'] = self.benefice_per_day(
                VenteModel, ProductModel)
            context['benefice_month'] = self.benefice_per_month(
                VenteModel, ProductModel)
        else:
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date', is_superuser=False, uname=user.username)
            context['dataset_depot'] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='DV', dt_col_name='created_date', is_superuser=False, uname=user.username)
            context["dataset_achat"] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='AD', dt_col_name='created_date', is_superuser=False, uname=user.username)
            context["achat_directs"] = ProductModel.objects.filter(
                shop__owner__user__username=user.username, dv_or_ad='AD').order_by('-created_date')
            context["depot_ventes"] = ProductModel.objects.filter(
                shop__owner__user__username=user.username, dv_or_ad='DV').order_by('-created_date')
            context["ventes"] = VenteModel.objects.filter(
                produit__shop__owner__user__username=user.username).order_by('-created_date')
            context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=user.username).values(
                'produit__name').annotate(freq=Count('produit__name')).order_by()
            context["tendance_achat_direct"] = ProductModel.objects.filter(
                shop__owner__user__username=user.username, dv_or_ad='AD').values('name').annotate(freq=Count('name')).order_by()
            context["n_product"] = ProductModel.objects.filter(
                shop__owner__user__username=user.username).count()
            context["n_client"] = ClientModel.objects.filter(
                shop__owner__user__username=user.username).count()
            context['benefice_day'] = self.benefice_per_day(
                VenteModel, ProductModel, is_superuser=False, user=user)
            context['benefice_month'] = self.benefice_per_month(
                VenteModel, ProductModel, is_superuser=False, user=user)
        return context


class AchatDirectView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'dashboard/achat_direct/achat_direct.html'
    model = ProductModel
    fields = '__all__'
    queryset = ProductModel.objects.filter(dv_or_ad='AD')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Achat Direct"
        uname = self.request.user.username
        if self.request.user.is_superuser:
            context['achat_directs'] = self.q = ProductModel.objects.filter(dv_or_ad='AD').order_by(
                '-created_date')
            # context['achat_directs'] = self.q = ProductModel.objects.filter(dv_or_ad = 'AD').order_by(
            #     '-created_date')
            context['count_item'] = self.q.count()
            context["tendance_achat_direct"] = ProductModel.objects.filter(dv_or_ad='AD').values(
                'name').annotate(freq=Count('name')).order_by("?")
            context['spent'] = sum(
                [p.price_total_tt_produit for p in self.q if p.price_total_tt_produit != None])
            context["dataset_achat_direct"] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='AD', dt_col_name='created_date')
        else:
            context['achat_directs'] = self.q = ProductModel.objects.filter(dv_or_ad='AD', shop__owner__user__username=uname).order_by(
                '-created_date')
            # context['achat_directs'] = self.q = ProductModel.objects.filter(dv_or_ad = 'AD').order_by(
            #     '-created_date')
            context['count_item'] = self.q.count()
            context["tendance_achat_direct"] = ProductModel.objects.filter(dv_or_ad='AD', shop__owner__user__username=uname).values(
                'name').annotate(freq=Count('name')).order_by("?")
            context['spent'] = sum(
                [p.price_total for p in self.q if p.price_total != None])
            context["dataset_achat_direct"] = self.chartObject(
                ProductModel, key='price_total', dt_col_name='created_date', dv_or_ad='AD', uname=uname, is_superuser=False)
        return context


class AchatDirectUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'dashboard/achat_direct/achat_direct_edit.html'
    model = ProductModel
    fields = '__all__'
    queryset = ProductModel.objects.filter(dv_or_ad='AD')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)


class AchatDirectDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/achat_direct/achat_direct_detail.html'
    model = ProductModel
    context_object_name = 'achat_direct'
    queryset = ProductModel.objects.filter(dv_or_ad='AD')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Achat Direct"
        return context


class AchatDirectDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/achat_direct/achat_direct_delete.html'
    model = ProductModel
    queryset = ProductModel.objects.filter(dv_or_ad='AD')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Achat Direct"
        return context


# First, creating the DepotVenteView
class DepotVenteView(LoginRequiredMixin, RedirectToPreviousMixin, TemplateView, Utils):
    template_name = 'dashboard/depot_vente/depot_vente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Depot Vente"
        uname = self.request.user.username
        if self.request.user.is_superuser:
            self.q = ProductModel.objects.order_by(
                '-created_date').filter(dv_or_ad='DV')
            context["tendance_depot_vente"] = ProductModel.objects.filter(dv_or_ad='DV').values(
                'name').annotate(freq=Count('name')).order_by("?")
            # Nombre de produit
            context['depot_ventes'] = self.q
            context['total_item'] = self.q.count()
            # Sum des produits de depots ventes
            context['spent_depot'] = sum(
                [p.price_total_tt_produit for p in self.q if p.price_total_tt_produit != None])
            context['dataset_depot'] = self.chartObject(
                ProductModel, key='price_total_tt_produit', dv_or_ad='DV', dt_col_name='created_date')
        else:
            self.q = ProductModel.objects.order_by(
                '-created_date').filter(dv_or_ad='DV', shop__owner__user__username=uname)
            context["tendance_depot_vente"] = ProductModel.objects.filter(dv_or_ad='DV', shop__owner__user__username=uname).values(
                'name').annotate(freq=Count('name')).order_by("?")
            # Nombre de produit
            context['depot_ventes'] = self.q
            context['total_item'] = self.q.count()
            # Sum des produits de depots ventes
            context['spent_depot'] = sum(
                [p.price_total for p in self.q if p.price_total != None])
            context["dataset_depot"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date', uname=uname, is_superuser=False)
        return context


# Second, create the DepotVenteDetailView
class DepotVenteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/depot_vente/depot_vente_detail.html'
    model = ProductModel
    context_object_name = 'd_vente'
    queryset = ProductModel.objects.filter(dv_or_ad='DV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Depot Vente"
        return context


# Third, create the depotVenteStockEditView
class DepotVenteEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    template_name = 'dashboard/depot_vente/depot_vente_edit.html'
    model = ProductModel
    fields = '__all__'
    queryset = ProductModel.objects.filter(dv_or_ad='DV')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Depot Vente"
        return context


class DepotVenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    model = ProductModel
    template_name = 'dashboard/depot_vente/depot_vente_delete.html'
    context_object_name = 'dv_delete'
    queryset = ProductModel.objects.filter(dv_or_ad='DV')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Depot Vente"
        return context


class ProductView(LoginRequiredMixin, CreateView):

    form_class = ProductModelForm
    template_name = 'dashboard/product/product.html'
    success_url = reverse_lazy('dashboard:productPage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        messages.success(self.request, 'Produit a été ajouté avec success')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Produit"
        u_user = self.request.user
        if u_user.is_superuser:
            context["products"] = ProductModel.objects.all()
        else:
            context["products"] = ProductModel.objects.filter(
                shop__owner__user__username=u_user.username)
        return context


class ProductUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'
    
    def get_success_url(self):
        product = ProductModel.objects.get(pk=self.kwargs["pk"])
        messages.success(self.request, "Produit {} a été modifié avec success.".format(product.name))
        return reverse('dashboard:productDetailPage', args=(self.kwargs["pk"],))

    def form_valid(self, form):
        user = self.request.user
        if not user.is_superuser:
            form.instance.shop = Shop.objects.get(
                ower__user__username=user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Produit"
        return context


class ProductDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # deleting a product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Produit"
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/product/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        u_user = self.request.user
        if not u_user.is_superuser:
            self.product = ProductModel.objects.filter(pk=self.kwargs["pk"],
                                                       shop__owner__user__username=u_user.username)
        else:
            self.product = ProductModel.objects.filter(pk=self.kwargs["pk"])
        return self.product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Produit"
        return context

# Rendering the pdf class here:


class GeneratePDF(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/invoice/invoice.html'
    model = VenteModel
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['v_shop'] = self.s = Shop.objects.all()

        context["f_number"] = self.kwargs["pk"]


        vente_of_that_date = VenteModel.objects.filter(
            client__pk=self.kwargs["pk"], 
            created_date__day=self.kwargs["day"],
            created_date__month=self.kwargs["month"],
            created_date__year=self.kwargs["year"],
        )

        context["ventes"] = vente_of_that_date
        context["v"] = v = vente_of_that_date[0] 
        acompte = any([True for v in vente_of_that_date if v.acompte > 0])
        c = 0
        

        if acompte:
            context["acompte"] = acompte
            context["total_acompte"] = c = sum([v.acompte for v in vente_of_that_date])

       
        total = sum(
            [v.price_total for v in vente_of_that_date if v.price_total]) - c

        if v.produit.estate == 'NEUF':
            tva = 0
        else :
            tva = total * 18 / 100
        

        context["total_price"] = sum(
            [v.price_total for v in vente_of_that_date if v.price_total]) - c + tva

        context ['tva'] = tva
        context ['total'] = total

        context['quantity'] = sum([qty.quantity for qty in vente_of_that_date])
        return context


"""
Here Is where we are going to make our models to be able to delete multiple times
"""


# Delete Multiple Product
def multiple_delete_product(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('id[]')
        for id in product_ids:
            product = ProductModel.objects.get(pk=id)
            product.delete()
    return redirect('dashboard:homePage')

# Delete Multiple  DepotVente


def multiple_delete_depotVente(request):
    if request.method == 'POST':
        depot_vente_ids = request.POST.getlist('id[]')
        for id in depot_vente_ids:
            dv = ProductModel.objects.filter(dv_or_ad='DV').get(pk=id)
            dv.delete()
    return redirect('dashboard:homePage')


# Delete Multiple AchatDirect
def multiple_delete_achatDirect(request):
    if request.method == 'POST':
        achat_direct_ids = request.POST.getlist('id[]')
        for id in achat_direct_ids:
            ad = ProductModel.objects.filter(dv_or_ad='AD').get(pk=id)
            ad.delete()
    return redirect('dashboard:homePage')

# Error handling


def custom_page_not_found_view(request, exception):
    response = render(request, 'dashboard/error/404.html', {})
    response.status_code = 404
    return response

