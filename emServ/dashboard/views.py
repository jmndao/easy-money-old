from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages

<<<<<<< HEAD
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from django.views.generic import (  TemplateView, 
                                    ListView, 
                                    DetailView,
                                    FormView
                                )

from django.views.generic.edit import ( CreateView,
                                        UpdateView,
                                        DeleteView,

                                    )
from dashboard.models import ProductModel,ClientModel
=======
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  FormView
                                  )
from django.views import View
from django.views.generic.detail import SingleObjectMixin
>>>>>>> akhadtop

from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                       )
from dashboard.models import ProductModel,ClientModel
from dashboard.forms import ProductModelForm,ClientModelForm


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

########## Product View: 
#
# Setting Logic:
#-------------------------: * Functions
#  - ProductView:           Route to product page 
#                           * Form (to add new product)
#                           * List (list all products) -> Detail
#  - ProductUpdateView:     Route to product update page
#                           * Update a product
#  - ProductDeleteView:     Route to product delete page
#                           * Delete a product
##########################################################
#
class ProductView(FormView, ListView):

    model = ProductModel
    context_object_name = 'products'
    form_class = ProductModelForm
    template_name = 'dashboard/product/product.html'

    def get_success_url(self):
        return reverse('dashboard:productDetailPage', {'pk', self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)

    # def get_queryset(self):
    #     # This below will take place in the future because
    #     # each shop has it owner and must only list for his shop
    #     # self.products = get_object_or_404()
    #     # self.owner =  ...
    #     # return Shop.object.filter(owner=self.owner)


class ProductUpdateView(UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'
    # Url to redirect after successfully
    # updating a product
    success_url = '/'


class ClientView(FormView, ListView):

    context_object_name = 'clients'
    form_class = ClientModelForm
    template_name = 'dashboard/client/client.html'
    queryset = ClientModel.objects.all()


    def get_success_url(self):
        return reverse('dashboard:productDetailPage', {'pk', self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)


class ProductDeleteView(DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # Url to redirect after successful
    # deleting a product
    success_url = '/'

class ClientView(ListView):
    model =  ClientModel
    template_name = 'dashboard/client/client_view.html'

class ProductDetailView(DetailView):

    model = ProductModel
    template_name = 'dashboard/product/product_detail.html'

#
########## End of Product View


def buyingStock(request):
    """
        Fonction    : Stock Achat
        Model       : - BuyingStockModel

        Context     : 
    """

    return render(request, "dashboard/buying.html", {})

