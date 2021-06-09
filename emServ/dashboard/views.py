from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  FormView
                                  )
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                       )
from dashboard.models import ProductModel,ClientModel

# Create your views here.


class IndexView(TemplateView):

    template_name = 'dashboard/index.html'


def profile(request):
    """
        Fonction    : Profile Utilisateur
        Model       : - User
                      - Profile
        Context     : 
    """

    return render(request, "dashboard/profile.html", {})


def client(request):
    """
        Fonction    : Gestion de Client
        Model       : - ClientModel

        Context     : 
    """

    return render(request, "dashboard/client.html", {})


def clientRequest(request):
    """
        Fonction    : Demande Client
        Model       : - ClientRequestModel
                      - ClientModel  
        Context     : 
    """

    return render(request, "dashboard/client_request.html", {})


class ProductDeposit(TemplateView):
    """
        Fonction    : Stock Depot
        Model       : - DepositStockModel

        Context     : 
    """
    template_name = 'dashboard/deposit.html'



class ProductView(CreateView):

    model = ProductModel
    template_name = 'dashboard/product/product.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard:productPage')

    def form_valid(self, form):
        # Future 
        # form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductModel.objects.order_by('created_date')
        context['title'] = 'Espace Produit'
        return context


class ProductUpdateView(UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'
    # Url to redirect after successfully
    # updating a product
    success_url = reverse_lazy('dashboard:productPage')


class ProductDeleteView(DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # Url to redirect after successful
    # deleting a product
    success_url = reverse_lazy('dashboard:productPage')


class ProductDetailView(DetailView):

    model = ProductModel
    template_name = 'dashboard/product/product_detail.html'
    

class ClientView(CreateView):

    template_name = 'dashboard/client/client.html'
    model = ClientModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:clientPage')

    def form_valid(self, form):
        # Future
        # form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Future
        # context['clients']  = ClientModel.objects.order_by('created_date')
        context['clients'] = ClientModel.objects.all()
        context['title'] = 'Espace Client'
        return context

class ClientUpdateView(UpdateView):

    template_name = 'dashboard/client/client_edit.html'
    fields = '__all__'
    model = ClientModel
    success_url = reverse_lazy('dashboard:clientPage')


class ClientDeleteView(DeleteView):

    template_name = 'dashboard/client/client_delete.html'
    model = ClientModel
    success_url = reverse_lazy('dashboard:clientPage')


class ClientDetailView(DetailView):

    template_name = 'dashboard/client/client_detail.html'
    model = ClientModel

def buyingStock(request):
    """
        Fonction    : Stock Achat
        Model       : - BuyingStockModel

        Context     : 
    """

    return render(request, "dashboard/buying.html", {})

