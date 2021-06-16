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
                                AchatDirectModel,
                                DepotVenteModel,
                                VenteModel,
                                Shop
                            )

from notifications.signals import notify

# Thhis is top adding the form
from .forms import DepotVenteModel

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


class AchatDirectView(LoginRequiredMixin, CreateView):

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
        rev = VenteModel.objects.all()
        sum_rv = sum([p.prix_de_vente_fin for p in rev])
        the_benefice = sum_rv - (spent_direct + achat_direct)
        return the_benefice 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_stocks'] = self.q = DepositStockModel.objects.order_by('-date_d_achat')
        context['count_item'] = self.q.count()
        context['spent'] = sum([p.prix_d_achat for p in self.q])
        context['benefice'] = self.benefice(context['spent'])
        return context


class AchatDirectUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/deposit_stock/deposit_stock_edit.html'
    model = AchatDirectStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depositStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AchatDirectDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/deposit_stock/deposit_stock_detail.html'
    model = DepositStockModel
    context_object_name = 'deposit'



class AchatDirectDeleteView(LoginRequiredMixin, DeleteView):

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

# First, creating the DepotVenteView
class DepotVenteStockView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock.html'
    model = DepotVenteStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depotVenteStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def benefice (self, d_vente_one):
        self.a_direct = DepositStockModel.objects.order_by('-date_d_achat')
        spent_two = sum([p.prix_d_achat for p in self.a_direct])
        rev = VenteModel.objects.all()
        sum_rv = sum([p.prix_de_vente_fin for p in rev])
        the_benefice = sum_rv - (d_vente_one + spent_two)
        return the_benefice 



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.q = DepotVenteStockModel.objects.order_by('-date_d_depot')
        
        #Nombre de produit
        context['depot_vente_stocks'] = self.q
        context['total_item'] = self.q.count()

        #Sum des produits de depots ventes
        spent_one = [p.prix_d_depot for p in self.q]
        spent_one_t = sum(spent_one)
        context['spent_depot'] = sum(spent_one)       

        #benefice
        self.a_direct = DepositStockModel.objects.order_by('-date_d_achat')
        spent_two = [p.prix_d_achat for p in self.a_direct]
        spent_two_t = sum(spent_two)
        context['spent_two_t'] = spent_two_t
         
        
        context['benefice'] = self.benefice(context['spent_depot'])
        return context


#Second, create the depotVenteStockCreateView



class VenteView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/vente/vente.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:VentePage')
    

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
        context['vente'] = self.q = VenteModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['revenue'] = sum([p.prix_de_vente_fin for p in self.q])
        context['benefice_two'] = self.benefice_two(context['revenue'])
        return context


class VenteUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'dashboard/vente/vente_edit.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:ventePage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VenteDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/vente/vente_detail.html'
    model = VenteModel
    context_object_name = 'sales'



class VenteDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'dashboard/vente/vente_delete.html'
    model = VenteModel
    success_url = reverse_lazy('dashboard:ventePage')


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
