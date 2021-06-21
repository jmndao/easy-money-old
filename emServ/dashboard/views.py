import datetime
from django.utils import timezone


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
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
                                AchatDirectModel,
                                DepotVenteModel,
                                VenteModel,
                                Shop
                            )

from dashboard.utils import Utils, RedirectToPreviousMixin


# Rendering the pdf file
from django.template.loader import get_template
from django.http import HttpResponse



# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView, Utils):

    template_name = 'dashboard/index.html'

    #benefice par mois
    def benefice_per_day(self, db_vente, db_depot, db_achat):
        """
        Calculate the Total benefice of the Shop:
            db_vente : is the Sales Model object (VenteModel)
            db_depot : is the Depot Vente Model object (DepotVenteModel)
            db_achat : is the total sum of all Achat Direct Model (AchatDirectModel) 
        """
        today = datetime.date.today()
        vente = db_vente.objects.filter(
                           created_date__day=today.day)
        depot = db_depot.objects.filter(
                           created_date__day=today.day)
        achat = db_achat.objects.filter(
                           created_date__day=today.day)
        sum_vente = sum([p.price for p in vente if p.price != None])
        sum_depot = sum([p.price for p in depot if p.price != None])
        sum_achat = sum([p.price for p in achat if p.price != None])
        return (sum_vente - (sum_depot + sum_achat))
    
    def benefice_per_month(self, db_vente, db_depot, db_achat):
        """
        Calculate the Total benefice of the Shop:
            db_vente : is the Sales Model object (VenteModel)
            db_depot : is the Depot Vente Model object (DepotVenteModel)
            db_achat : is the total sum of all Achat Direct Model (AchatDirectModel) 
        """
        today = datetime.date.today()
        vente = db_vente.objects.filter(
                           created_date__month=today.month)
        depot = db_depot.objects.filter(
                           created_date__month=today.month)
        achat = db_achat.objects.filter(
                           created_date__month=today.month)
        sum_vente = sum([p.price for p in vente if p.price != None])
        sum_depot = sum([p.price for p in depot if p.price != None])
        sum_achat = sum([p.price for p in achat if p.price != None])
        return (sum_vente - (sum_depot + sum_achat))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        context = super().get_context_data(**kwargs)
        context['benefice_day'] = self.benefice_per_day(VenteModel, DepotVenteModel, AchatDirectModel)
        context['benefice_month'] = self.benefice_per_month(VenteModel, DepotVenteModel, AchatDirectModel)

        if self.request.user.is_superuser:
            context["achat_directs"] = AchatDirectModel.objects.all().order_by('-created_date')
            context["ventes"] = VenteModel.objects.all().order_by('-created_date')
            context["dataset_achat"] = self.chartObject(VenteModel, key='price', dt_col_name='created_date')
            context['dataset_depot'] = self.chartObject(DepotVenteModel, key = 'price', dt_col_name = 'created_date')
            context["dataset_stock"] = self.chartObject(AchatDirectModel, key='price', dt_col_name='created_date')
            context["tendance_vente"] = VenteModel.objects.values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["tendance_achat_direct"] = AchatDirectModel.objects.values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["n_product"] = ProductModel.objects.all().count()
            context["n_client"] = ClientModel.objects.all().count()
        else: 
            context["achat_directs"] = AchatDirectModel.objects.filter(produit__shop__owner__user__username=uname).order_by('-created_date')
            context["ventes"] = VenteModel.objects.filter(produit__shop__owner__user__username=uname).order_by('-created_date')
            context["dataset_achat"] = self.chartObject(VenteModel, key='price', dt_col_name='created_date', uname=uname, is_superuser=False)
            context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=uname).values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["tendance_achat_direct"] = AchatDirectModel.objects.filter(produit__shop__owner__user__username=uname).values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["n_product"] = ProductModel.objects.filter(shop__owner__user__username=uname).count()
            context["n_client"] = ClientModel.objects.filter(shop__owner__user__username=uname).count()
        
        #Having the benefice
        
        return context



class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/profile.html'


class ClientRequestView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):

    template_name = 'dashboard/client_request/client_request.html'
    model = ClientRequestModel
    fields = '__all__'
    
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            uuser = self.request.user
            if uuser.is_superuser:
                # What the super Admin will see
                context["client_requests"] = ClientRequestModel.objects.all()
            else:
                # What the simple Admin will see
                context["client_requests"] = ClientRequestModel.objects.filter(client__shop__owner__user__username=uuser.username)
            # What both will
            return context


class ClientRequestUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'dashboard/client_request/client_request_edit.html'
    model = ClientRequestModel
    fields = '__all__'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(owner__user__username=self.request.user.username)
        return super().form_valid(form)


class ClientRequestDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/client_request/client_request_detail.html'
    model = ClientRequestModel
    
    def get_queryset(self):
        uname = self.request.user.username
        self.client_request = get_object_or_404(ClientRequestModel, 
                                                pk=self.kwargs['pk'],
                                                client__shop__owner__user__username=uname)
        return self.client_request
    


class ClientRequestDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/client_request/client_request_delete.html'
    model = ClientRequestModel



class AchatDirectView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'dashboard/achat_direct/achat_direct.html'
    model = AchatDirectModel
    fields = '__all__'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit_stocks'] = self.q = AchatDirectModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['spent'] = sum([p.price for p in self.q if p.price != None])
        context['benefice'] = self.benefice_achat_direct(VenteModel, DepotVenteModel, context['spent'])
        if self.request.user.is_superuser:
            context["dataset_achat_direct"] = self.chartObject(AchatDirectModel, key='price', dt_col_name='created_date')
        else:
            context["dataset_achat_direct"] = self.chartObject(AchatDirectModel, key='price', dt_col_name='created_date', uname=uname, is_superuser=False)
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
    context_object_name = 'deposit'



class AchatDirectDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/achat_direct/achat_direct_delete.html'
    model = AchatDirectModel



# First, creating the DepotVenteView
class DepotVenteView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):
    template_name = 'dashboard/depot_vente/depot_vente.html'
    model = DepotVenteModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        self.q = DepotVenteModel.objects.order_by('-created_date')    

        #Nombre de produit
        context['depot_ventes'] = self.q
        context['total_item'] = self.q.count()
        #Sum des produits de depots ventes
        context['spent_depot'] = sum([p.price for p in self.q if p.price != None])
        #benefice 
        context['benefice'] = self.benefice_depot_vente(AchatDirectModel, VenteModel, context['spent_depot'])
        if self.request.user.is_superuser:
            context["dataset_depot"] = self.chartObject(DepotVenteModel, key='price', dt_col_name='created_date')
        else:
            context["dataset_depot"] = self.chartObject(DepotVenteModel, key='price', dt_col_name='created_date', uname=uname, is_superuser=False)
        return context



#Second, create the DepotVenteDetailView
class DepotVenteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/depot_vente/depot_vente_detail.html'
    model = DepotVenteModel
    context_object_name = 'd_vente'



#Third, create the depotVenteStockEditView    
class DepotVenteEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    template_name = 'dashboard/depot_vente/depot_vente_edit.html'
    model = DepotVenteModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DepotVenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    model = ProductModel
    template_name = 'dashboard/depot_vente/depot_vente_delete.html'
    context_object_name = 'dv_delete'



class VenteView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'dashboard/vente/vente.html'
    model = VenteModel
    fields = '__all__'    

    def form_valid(self, form):
        u_user = self.request.user
        if not u_user.is_superuser:
            form.instance.shop = Shop.objects.get(owner__user__username=u_user.username)
        product = ProductModel.objects.get(pk=form.instance.produit.pk)
        product.sold = True 
        product.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vente'] = self.q = VenteModel.objects.order_by('-created_date')
        context['count_item'] = self.q.count()
        context['revenue'] = sales = sum([p.price for p in self.q if p.price != None])
        context['benefice'] = self.benefice_vente(AchatDirectModel, DepotVenteModel, sales)

        uname = self.request.user.username
        if self.request.user.is_superuser:
            context["dataset_vente"] = self.chartObject(VenteModel, key='price', dt_col_name='created_date')
        else:
            context["dataset_vente"] = self.chartObject(VenteModel, key='price', dt_col_name='created_date', uname=uname, is_superuser=False)


           
        return context


class VenteUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'dashboard/vente/vente_edit.html'
    model = VenteModel
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VenteDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/vente/vente_detail.html'
    model = VenteModel
    context_object_name = 'sales'



class VenteDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/vente/vente_delete.html'
    model = VenteModel



class ProductView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):

    model = ProductModel
    template_name = 'dashboard/product/product.html'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Verify form is valid
        if form.is_valid():
            # Call parent form_valid to create model record object
            u_user = self.request.user
            if not u_user.is_superuser:
                form.instance.shop = Shop.objects.get(shop__owner__user__username=u_user.username)
            super().form_valid(form)
            # latest record
            latest_record = ProductModel.objects.last()
            if form.instance.dv_or_ad == 'DV':
                DepotVenteModel(
                    produit = latest_record,
                    price = latest_record.price
                ).save()
            else:
                AchatDirectModel(
                    produit = latest_record,
                    price = latest_record.price,
                    client = latest_record.client
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
        u_user = self.request.user
        if u_user.is_superuser:
            context["products"] = ProductModel.objects.all()
        else:
            context["products"] = ProductModel.objects.filter(shop__owner__user__username=u_user.username)
        return context


class ProductUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    model = ProductModel
    template_name = 'dashboard/product/product_edit.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        


class ProductDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    model = ProductModel
    template_name = 'dashboard/product/product_delete.html'
    # deleting a product
    context_object_name = 'product'



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
    
    

class ClientView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'dashboard/client/client.html'
    model = ClientModel
    fields = '__all__'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop = Shop.objects.get(owner__user__username=self.request.user.username)
            form.instance.shop = shop
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        if self.request.user.is_superuser:
            # What the superAdmin will see
            context['clients'] = self.c = ClientModel.objects.all()
            context['c_number'] = count = self.c.count()
        else:
            # What the simpleAdmin sill see
            context['clients'] = ClientModel.objects.filter(shop__owner__user__username=uname)

        # What both will see
        context['title'] = 'Espace Client'
        if self.request.user.is_superuser:
            context["dataset_client"] = self.chartObject(ClientModel, key='passage', dt_col_name='created_date')
        else:
            context["dataset_client"] = self.chartObject(ClientModel, key='passage', dt_col_name='created_date', uname=uname, is_superuser=False)
        return context

class ClientUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'dashboard/client/client_edit.html'
    fields = '__all__'
    model = ClientModel

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class ClientDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/client/client_delete.html'
    model = ClientModel



class ClientDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/client/client_detail.html'
    model = ClientModel



#Rendering the pdf class here:
class GeneratePDF(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/invoice/invoice.html'

    model = ClientModel
    fields = '__all__'

    # def get(self, *args, **kwargs):
    #     template = get_template('dashboard/invoice/invoice.html')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['all_vente'] = self.a = VenteModel.objects.all()
        context['f_number'] = self.a.count()


        # context['v_shop'] = self.s = Shop.objects.all()


        context['vente'] = self.q = VenteModel.objects.last()
        context['c_fname'] = self.q.client.fname
        context['c_lname'] = self.q.client.lname
        context['c_price'] = self.q.price
        context['v_date'] = date =self.q.created_date
        date =  date.strftime("%B-%d")
        context['v_date'] = date
        context['c_address'] = self.q.client.address
        context['c_tel'] = self.q.client.numero
        context['v_product'] = self.q.produit.name
        

        context['quantity'] = 1
        
        
        
        ################################################################
       
        return context
        
        # vente = get_object_or_404(VenteModel, pk=self.kwargs['pk'])
        # context = {
        #     'vente':vente,
        #     'invoice_id' : 123,
        #     'customer_name' : 'akhad', 
        # }
        # pdf = self.render_to_pdf('dashboard/invoice/invoice.html', context)
        # if pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     filename = "Invoice_%s.pdf" %("facture easy money")
        #     content = "inline; filename='%s'" %(filename)
        #     download = self.request.GET.get("download")
        #     if download:
        #         content = "attachment; filename='%s'" %(filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return pdf