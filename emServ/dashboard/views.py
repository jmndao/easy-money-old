from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  FormView
                                  )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                       )
from dashboard.models import (  ProductModel, 
                                ClientModel,
                                ClientRequestModel,
                                DepositStockModel,
                                DepotVenteStockModel,
                                BuyingStockModel,
                                Shop
                            )

from notifications.signals import notify

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/index.html'


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


class DepositStockView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/deposit_stock/deposit_stock.html'
    model = DepositStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depositStockPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def benefice(self, sum_dp):
        rev = BuyingStockModel.objects.all()
        sum_rev = sum([p.prix_de_vente_fin for p in rev])
        return (sum_rev - sum_dp)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_stocks'] = self.q = DepositStockModel.objects.order_by('-date_d_achat')
        context['count_item'] = self.q.count()
        context['spent'] = sum([p.prix_d_achat for p in self.q])
        context['benefice'] = self.benefice(context['spent'])
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

    # def get_success_url(self):
    #     notify.send(
    #         self.request.user,
    #         recipient=self.request.,
    #         description=form.instance.text_message,
    #         verb=form.instance.subject
    #     )
    #     return super().get_success_url()


# For the new depot vente tab that I am creating.

class DepotVenteStockView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock.html'
    model = DepotVenteStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depotVenteStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

 
class BuyingStockView(LoginRequiredMixin, CreateView):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buying_stocks'] = self.q = BuyingStockModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['revenue'] = sum([p.prix_de_vente_fin for p in self.q])
        context['benefice'] = self.benefice(context['revenue'])
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
