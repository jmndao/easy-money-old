import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Count
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import (TemplateView,
                                  DetailView,
                                  ListView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from dashboard.models import (ProductModel,
                              ClientRequestModel,
                              AchatDirectModel,
                              DepotVenteModel,
                              VenteModel,
                              Shop,
                              DevisModel,
                              EstimationModel)
from clients.models import ClientModel
from dashboard.utils import Utils, RedirectToPreviousMixin
from django.contrib import messages
from dashboard.forms import VenteForm, ProductModelForm, DevisModelForm
from django.shortcuts import redirect


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
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date')
            context["dataset_achat"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='AD', dt_col_name='created_date')
            context["achat_directs"] = AchatDirectModel.objects.all().order_by(
                '-created_date')
            context["depot_ventes"] = DepotVenteModel.objects.all().order_by(
                '-created_date')
            context["ventes"] = VenteModel.objects.all().order_by(
                '-created_date')
            context["tendance_vente"] = VenteModel.objects.values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
            context["tendance_achat_direct"] = AchatDirectModel.objects.values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
            context["tendance_depot_vente"] = DepotVenteModel.objects.values(
                'produit__name').annotate(freq=Count('produit__name')).order_by("?")
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
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date' , is_superuser=False, uname=user.username)
            context["dataset_achat"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='AD', dt_col_name='created_date', is_superuser=False, uname=user.username)
            context["achat_directs"] = AchatDirectModel.objects.filter(
                produit__shop__owner__user__username=user.username).order_by('-created_date')
            context["depot_ventes"] = DepotVenteModel.objects.filter(
                produit__shop__owner__user__username=user.username).order_by('-created_date')
            context["ventes"] = VenteModel.objects.filter(
                produit__shop__owner__user__username=user.username).order_by('-created_date')
            context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=user.username).values(
                'produit__name').annotate(freq=Count('produit__name')).order_by()
            context["tendance_achat_direct"] = AchatDirectModel.objects.filter(
                produit__shop__owner__user__username=user.username).values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["n_product"] = ProductModel.objects.filter(
                shop__owner__user__username=user.username).count()
            context["n_client"] = ClientModel.objects.filter(
                shop__owner__user__username=user.username).count()
            context['benefice_day'] = self.benefice_per_day(
                VenteModel, ProductModel, is_superuser=False, user=user)
            context['benefice_month'] = self.benefice_per_month(
                VenteModel, ProductModel, is_superuser=False, user=user)

        # Having the benefice

        return context


class ClientRequestView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/client_request/client_request.html'
    model = ClientRequestModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:clientRequestPage')
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Demande Client"
        uuser = self.request.user
        if uuser.is_superuser:
            # What the super Admin will see
            context["client_requests"] = ClientRequestModel.objects.all()
        else:
            # What the simple Admin will see
            context["client_requests"] = ClientRequestModel.objects.filter(
                client__shop__owner__user__username=uuser.username)
        # What both will
        return context


class ClientRequestUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'dashboard/client_request/client_request_edit.html'
    model = ClientRequestModel
    fields = '__all__'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Demande Utilisateur"
        return context
    


class ClientRequestDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/client_request/client_request_detail.html'
    model = ClientRequestModel

    def get_queryset(self):
        uname = self.request.user.username
        self.client_request = get_object_or_404(ClientRequestModel,
                                                pk=self.kwargs['pk'],
                                                client__shop__owner__user__username=uname)
        return self.client_request
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Demande Utilisateur"
        return context
    


class ClientRequestDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/client_request/client_request_delete.html'
    model = ClientRequestModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Demande Utilisateur"
        return context
    


class AchatDirectView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'dashboard/achat_direct/achat_direct.html'
    model = AchatDirectModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
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
                [p.price_total for p in self.q if p.price_total != None])
            context["dataset_achat_direct"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='AD', dt_col_name='created_date')
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
    model = AchatDirectModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AchatDirectDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/achat_direct/achat_direct_detail.html'
    model = AchatDirectModel
    context_object_name = 'achat_direct'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Achat Direct"
        return context
    


class AchatDirectDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/achat_direct/achat_direct_delete.html'
    model = AchatDirectModel

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
            self.q = ProductModel.objects.order_by('-created_date').filter(dv_or_ad = 'DV')
            context["tendance_depot_vente"] = ProductModel.objects.filter(dv_or_ad ='DV').values(
                'name').annotate(freq=Count('name')).order_by("?")
            # Nombre de produit
            context['depot_ventes'] = self.q
            context['total_item'] = self.q.count()
            # Sum des produits de depots ventes
            context['spent_depot'] = sum(
                [p.price_total for p in self.q if p.price_total != None])
            context['dataset_depot'] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date')
        else:
            self.q = ProductModel.objects.order_by('-created_date').filter(dv_or_ad = 'DV', shop__owner__user__username=uname)
            context["tendance_depot_vente"] = ProductModel.objects.filter(dv_or_ad ='DV', shop__owner__user__username=uname).values(
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Depot Vente"
        return context
    


# Third, create the depotVenteStockEditView
class DepotVenteEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    template_name = 'dashboard/depot_vente/depot_vente_edit.html'
    model = ProductModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Depot Vente"
        return context
    


class DepotVenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    model = ProductModel
    template_name = 'dashboard/depot_vente/depot_vente_delete.html'
    context_object_name = 'dv_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Depot Vente"
        return context
    


class VenteView(LoginRequiredMixin, CreateView, Utils):

    template_name = 'dashboard/vente/vente.html'
    form_class = VenteForm
    success_url = reverse_lazy('dashboard:ventePage')

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
            messages.error(self.request, "Il ne reste que {} object(s) de {}".format(
                product.quantity, product.name))
        # elif remaining_qty == 0:
        #     ProductModel.objects.filter(pk=form.instance.produit.pk).delete()
        else:
            product.quantity = remaining_qty
            product.initial_quantity = product.quantity + vente_qty
        product.save()
        # Checking whether client has already passed or not
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

    template_name = 'dashboard/vente/vente_edit.html'
    model = VenteModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Vente"
        return context
    


class VenteDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/vente/vente_detail.html'
    model = VenteModel
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Vente"
        return context
    


class VenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/vente/vente_delete.html'
    model = VenteModel
    context_object_name = 'vente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Vente"
        return context
    


class ProductView(LoginRequiredMixin, CreateView):

    form_class = ProductModelForm
    template_name = 'dashboard/product/product.html'
    success_url = reverse_lazy('dashboard:productPage')

    def form_valid(self, form):
        # check if we choose the right quantities or not?
        ################################################################   
        initial_quantity = form.instance.quantity
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Verify form is valid
        if form.is_valid():
            # Call parent form_valid to create model record object
            u_user = self.request.user
            if not u_user.is_superuser:
                form.instance.shop = Shop.objects.get(
                    owner__user__username=u_user.username)
            super().form_valid(form)
            # latest record
            latest_record = ProductModel.objects.last()
            if form.instance.dv_or_ad == 'DV':
                DepotVenteModel(
                    produit=latest_record,
                    price=latest_record.price
                ).save()
            else:
                AchatDirectModel(
                    produit=latest_record,
                    price=latest_record.price,
                    # client = latest_record.client
                ).save()
            # messages.success(request, 'Item created successfully!')
            # Redirect to success page
            return HttpResponseRedirect(self.get_success_url())
        # Form is invalid
        # Set object to None, since class-based view expects model record object
        self.object = None
        # Return class-based view form_invalid to generate form with errors
        return self.form_invalid(form)

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

    def form_valid(self, form):
        form.instance.user = self.request.user
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
        context['all_vente'] = self.a = VenteModel.objects.all()
        context['f_number'] = self.a.count()
        # context['v_shop'] = self.s = Shop.objects.all()
        context['vente'] = self.q = VenteModel.objects.get(
            pk=self.kwargs["pk"])
        context['quantity'] = self.q.quantity
        context['c_fname'] = self.q.client.fname
        context['c_lname'] = self.q.client.lname
        context['c_price'] = self.q.price
        context['c_price_total'] = self.q.price_total
        context['v_date'] = date = self.q.created_date
        date = date.strftime("%B-%d")
        context['v_date'] = date
        context['c_address'] = self.q.client.address
        context['c_tel'] = self.q.client.numero
        context['v_product'] = self.q.produit.name
        ################################################################

        return context

# Rendering the devis class here


class GenerateDevis(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/devis/devis.html'
    form_class = DevisModelForm
    success_url = reverse_lazy('dashboard:devisPage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['devis'] = self.a = DevisModel.objects.all()
            context['d_number'] = self.a.count() 
        else:
            context['devis'] = self.a = DevisModel.objects.filter(shop__owner__user=user)
            context['d_number'] = self.a.count() 
        return context


class DevisDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    template_name = 'dashboard/devis/devisDelete.html'
    model = DevisModel
    context_object_name = 'devis'


class TirerDevis(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/devis/tirerDevis.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:devisPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_devis'] = self.a = DevisModel.objects.all()
        context['f_number'] = self.a.count()
        # context['v_shop'] = self.s = Shop.objects.all()
        context['devis'] = self.q = DevisModel.objects.get(
            pk=self.kwargs["pk"])
        context['quantity'] = self.q.quantity
        context['c_fname'] = self.q.client.fname
        context['c_lname'] = self.q.client.lname
        context['c_price'] = self.q.price
        context['c_price_total'] = self.q.price_total
        context['v_date'] = date = self.q.created_date
        date = date.strftime("%B-%d")
        context['v_date'] = date
        context['c_address'] = self.q.client.address
        context['c_tel'] = self.q.client.numero
        context['v_product'] = self.q.produit.name
        ################################################################

        return context


class EstimationPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/estimation.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:lastEstimationPage')

    def form_valid(self, form):
        form.instance.final_price = self.estimation_from_form(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Estimation"
        user = self.request.user
        if user.is_superuser:
            context['estimates'] = self.e = EstimationModel.objects.all()
        else:
            context['estimates'] = self.e = EstimationModel.objects.filter(shop__owner__user=user)
        return context
    

class LastEstimationPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/lastEstimation.html'
    model = EstimationModel
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estimates'] = self.q = EstimationModel.objects.last()
        context['estimation_result'] = self.estimation_from_model(EstimationModel, last=True)
        context['new_price'] = self.q.new_price
        context['name_product'] = self.q.product_name
        context['reparation'] = self.q.reparatinon_price
        return context

class EstimationDetail(LoginRequiredMixin, DetailView):
    model = EstimationModel
    template_name = 'dashboard/estimation/estimation_detail.html'
    context_object_name = 'estimation'

    def get_queryset(self):
        u_user = self.request.user
        if not u_user.is_superuser:
            self.estimation = EstimationModel.objects.filter(pk=self.kwargs["pk"],
                                                     shop__owner__user__username=u_user.username)
        else:
            self.estimation = EstimationModel.objects.filter(pk=self.kwargs["pk"])
        return self.estimation

class EstimationEdit(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/estimation/estimationEdit.html'
    fields = '__all__'
    model = EstimationModel
    success_url = reverse_lazy('dashboard:estimationPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EstimationResultPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/estimationResult.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:estimationPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_devis'] = self.a = EstimationModel.objects.all()
        context['e_number'] = self.a.count()
        context['estimates'] = self.q = EstimationModel.objects.get(
            pk=self.kwargs["pk"])
        context['estimation_result'] = self.estimation_from_model(EstimationModel, last=False, pk=self.kwargs["pk"])
        context['c_fname'] = self.q.seller
        context['c_address'] = self.q.address
        context['c_tel'] = self.q.numero
        context['v_date'] = date = self.q.created_date
        date = date.strftime("%B-%d")
        context['v_date'] = date
        context['v_product'] = self.q.product_name
        return context
    


class EstimationDeletePage(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/estimation/estimationDelete.html'
    model = EstimationModel
    context_object_name = 'estimates'


"""
Here Is where we are going to make our models to be able to delete multiple times
"""
#Delete Multiple Estimation
def multiple_delete_estimation(request):
    if request.method == 'POST':
        estimate_ids = request.POST.getlist('id[]')
        for id in estimate_ids:
            estimate = EstimationModel.objects.get(pk=id)
            estimate.delete()
    return redirect('dashboard:homePage')

#Delete Multiple Product
def multiple_delete_product(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('id[]')
        for id in product_ids:
            product = ProductModel.objects.get(pk=id)
            product.delete()
    return redirect('dashboard:homePage')

#Delete Multiple Vente
def multiple_delete_vente(request): 
    if request.method == 'POST':
        vente_ids = request.POST.getlist('id[]')
        for id in vente_ids:
            vente = VenteModel.objects.get(pk=id)
            vente.delete()
    return redirect('dashboard:homePage')

#Delete Multiple Delete ClientRequest
def multiple_delete_clientRequest(request):
    if request.method == 'POST':
        c_req_ids = request.POST.getlist('id[]')
        for id in c_req_ids:
            c_req = ClientRequestModel.objects.get(pk=id)
            c_req.delete()
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
