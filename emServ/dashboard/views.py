from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  FormView)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from dashboard.models import (  ProductModel, 
                                ClientModel,
                                ClientRequestModel,
                                DepositStockModel,
                                DepotVenteStockModel,
                                BuyingStockModel,
                                Shop)

from notifications.signals import notify
from dashboard.utils import Utils

# Thhis is top adding the form
from .forms import DepotVenteModel

class IndexView(LoginRequiredMixin, TemplateView, Utils):

    template_name = 'dashboard/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stocks"] = DepositStockModel.objects.all().order_by('-date_d_achat')
        context["achats"] = BuyingStockModel.objects.all().order_by('-created_date')
        context["dataset_achat"] = self.chartObject(BuyingStockModel, key='prix_de_vente_fin', dt_col_name='created_date')
        context["dataset_stock"] = self.chartObject(DepositStockModel, key='prix_d_achat', dt_col_name='date_d_achat')
        context["trend_achat"] = BuyingStockModel.objects.values('produit__nom_du_produit').annotate(freq=Count('produit__nom_du_produit')).order_by()
        context["trend_stock"] = DepositStockModel.objects.values('produit__nom_du_produit').annotate(freq=Count('produit__nom_du_produit')).order_by()
        context["n_product"] = ProductModel.objects.all().count()
        context["n_client"] = ClientModel.objects.all().count()
        return context
    


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/profile.html'


class ClientRequestView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/client_request/client_request.html'
    model = ClientRequestModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:clientRequestPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Future
            # context['client_requests'] = ClientRequestModel.objects.order_by('created_date')
            context["client_requests"] = ClientRequestModel.objects.all()
            return context


class ClientRequestUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/client_request/client_request_edit.html'
    model = ClientRequestModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:clientRequestPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientRequestDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/client_request/client_request_detail.html'
    model = ClientRequestModel



class ClientRequestDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'dashboard/client_request/client_request_delete.html'
    model = ClientRequestModel
    success_url = reverse_lazy('dashboard:clientRequestPage')


class DepositStockView(LoginRequiredMixin, CreateView, Utils):

    template_name = 'dashboard/deposit_stock/deposit_stock.html'
    model = DepositStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depositStockPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def benefice (self, achat_direct):
        self.d_vente = DepotVenteStockModel.objects.order_by('-date_d_depot')
        spent_direct = sum([p.prix_d_depot for p in self.d_vente])
        rev = BuyingStockModel.objects.all()
        sum_rv = sum([p.prix_de_vente_fin for p in rev])
        the_benefice = sum_rv - (spent_direct + achat_direct)
        return the_benefice 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_stocks'] = self.q = DepositStockModel.objects.order_by('-date_d_achat')
        context['count_item'] = self.q.count()
        context['spent'] = sum([p.prix_d_achat for p in self.q])
        context['benefice'] = self.benefice_stock(BuyingStockModel, context['spent'])
        return context


class DepositStockUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/deposit_stock/deposit_stock_edit.html'
    model = DepositStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depositStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DepositStockDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/deposit_stock/deposit_stock_detail.html'
    model = DepositStockModel
    context_object_name = 'deposit'


class DepositStockDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'dashboard/deposit_stock/deposit_stock_delete.html'
    model = DepositStockModel
    success_url = reverse_lazy('dashboard:depositStockPage')

    

class BuyingStockView(LoginRequiredMixin, CreateView, Utils):

    template_name = 'dashboard/buying_stock/buying_stock.html'
    model = BuyingStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:buyingStockPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def benefice(self, revenue):
        dp = DepositStockModel.objects.all()
        sum_dp = sum([p.prix_d_achat for p in dp])
        return (revenue - sum_dp)
    
    def benefice_two(self, revenue):
        self.d_vente = DepotVenteStockModel.objects.order_by('-date_d_depot')
        spent_direct = sum([p.prix_d_depot for p in self.d_vente])
        self.achat_direct = DepositStockModel.objects.all()
        sum_achat = sum([p.prix_d_achat for p in self.achat_direct])
        the_benefice = revenue - (spent_direct + sum_achat)
        return the_benefice 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buying_stocks'] = self.q = BuyingStockModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['revenue'] = sum([p.prix_de_vente_fin for p in self.q])
        context['benefice_two'] = self.benefice_two(context['revenue'])
        return context


class BuyingStockUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/buying_stock/buying_stock_edit.html'
    model = BuyingStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:buyingStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BuyingStockDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/buying_stock/buying_stock_detail.html'
    model = BuyingStockModel
    context_object_name = 'sales'



class BuyingStockDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'dashboard/buying_stock/buying_stock_delete.html'
    model = BuyingStockModel
    success_url = reverse_lazy('dashboard:buyingStockPage')


class ProductView(LoginRequiredMixin, CreateView):

    model = ProductModel
    template_name = 'dashboard/product/product.html'
    fields = '__all__'

    success_url = reverse_lazy('dashboard:productPage')

    def form_valid(self, form):
        # Future 
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductModel.objects.order_by('created_date')
        context['title'] = 'Espace Produit'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'
    # Url to redirect after successfully
    # updating a product
    success_url = reverse_lazy('dashboard:productPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # Url to redirect after successful
    # deleting a product
    context_object_name = 'product'
    success_url = reverse_lazy('dashboard:productPage')


class ProductDetailView(LoginRequiredMixin, DetailView):

    model = ProductModel
    template_name = 'dashboard/product/product_detail.html'
    context_object_name = 'product'
    

class ClientView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/client/client.html'
    model = ClientModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:clientPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Future
        # context['clients']  = ClientModel.objects.order_by('created_date')
        context['clients'] = ClientModel.objects.all()
        context['title'] = 'Espace Client'
        return context

class ClientUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/client/client_edit.html'
    fields = '__all__'
    model = ClientModel
    success_url = reverse_lazy('dashboard:clientPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'dashboard/client/client_delete.html'
    model = ClientModel
    success_url = reverse_lazy('dashboard:clientPage')



class ClientDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/client/client_detail.html'
    model = ClientModel
