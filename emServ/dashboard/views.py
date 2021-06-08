from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  FormView
                                  )

from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                       )
from dashboard.models import ProductModel


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


class ProductUpdateView(UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'
    # Url to redirect after successfully
    # updating a product
    success_url = '/'


class ProductDeleteView(DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # Url to redirect after successful
    # deleting a product
    success_url = '/'


def buyingStock(request):
    """
        Fonction    : Stock Achat
        Model       : - BuyingStockModel

        Context     : 
    """

    return render(request, "dashboard/buying.html", {})


def product(request):
    """
        Fonction    : Produit
        Model       : - ProdcutModel

        Context     : 
    """

    return render(request, "dashboard/produit.html", {})
