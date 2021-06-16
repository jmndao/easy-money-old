from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db.models import Count
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import (TemplateView,
                                  DetailView,
                                  View)
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

# from notifications.signals import notify
from dashboard.utils import Utils
# from dashboard.forms import DepotVenteModelForm




# Rendering the pdf file
from django.template.loader import get_template
from django.http import HttpResponse


# Create your views here.
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


class DepositStockView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/deposit_stock/deposit_stock.html'
    model = DepositStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depositStockPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_stocks'] = self.q = DepositStockModel.objects.order_by('-date_d_achat')
        context['count_item'] = self.q.count()
        context['spent'] = sum([p.prix_d_achat for p in self.q])
        context['benefice'] = self.benefice_stock(BuyingStockModel, DepotVenteStockModel, context['spent'])
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


# For the new depot vente tab that I am creating.

# First, creating the DepotVenteView
class DepotVenteStockView(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock.html'
    model = DepotVenteStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depotVenteStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.q = DepotVenteStockModel.objects.order_by('-date_d_depot')    
        #Nombre de produit
        context['depot_vente_stocks'] = self.q
        context['total_item'] = self.q.count()
        #Sum des produits de depots ventes
        context['spent_depot'] = sum([p.prix_d_depot for p in self.q])
        #benefice 
        context['benefice'] = self.benefice_dv(DepositStockModel, BuyingStockModel, context['spent_depot'])
        return context

    
    def benefice (self, d_vente_one):
        self.a_direct = DepositStockModel.objects.order_by('-date_d_achat')
        spent_two = sum([p.prix_d_achat for p in self.a_direct])
        rev = BuyingStockModel.objects.all()
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


#Second, create the depotVenteStockDetailView
class DepotVenteStockDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock_detail.html'
    model = DepotVenteStockModel
    context_object_name = 'd_vente'



#Third, create the depotVenteStockEditView    
class DepotVenteStockEditView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock_edit.html'
    model = DepotVenteStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:depotVenteStockPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DepotVenteStockDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductModel
    template_name = 'dashboard/depot_vente_stock/depot_vente_stock_delete.html'
    context_object_name = 'dv_delete'
    success_url = reverse_lazy('dashboard:depotVenteStockPage')

class BuyingStockView(LoginRequiredMixin, CreateView):

    template_name = 'dashboard/buying_stock/buying_stock.html'
    model = BuyingStockModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:buyingStockPage')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buying_stocks'] = self.q = BuyingStockModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['revenue'] = sales = sum([p.prix_de_vente_fin for p in self.q])
        context['benefice'] = self.benefice_sale(DepositStockModel, DepotVenteStockModel, sales)
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

#Rendering the pdf class here:
class GeneratePDF(View, Utils):
    def get(self, request, *args, **kwargs):
        template = get_template('dashboard/invoice/invoice.html')
        context = {
            'invoice_id' : 123,
            'customer_name' : 'akhad', 
            'today' : 'Today'
        }
        pdf = self.render_to_pdf('dashboard/invoice/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("facture easy money")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return pdf