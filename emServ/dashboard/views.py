import datetime
from django.shortcuts import get_object_or_404
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
                              ClientModel,
                              ClientRequestModel,
                              AchatDirectModel,
                              DepotVenteModel,
                              VenteModel,
                              Shop,
                              DevisModel,
                              EstimationModel)

from dashboard.utils import Utils, RedirectToPreviousMixin
from django.contrib import messages
from dashboard.forms import VenteForm


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView, Utils):

    template_name = 'dashboard/index.html'

    # benefice par mois
    # def benefice_per_day(self, db_vente, db_depot, db_achat):
    #     """
    #     Calculate the Total benefice of the Shop:
    #         db_vente : is the Sales Model object (VenteModel)
    #         db_depot : is the Depot Vente Model object (DepotVenteModel)
    #         db_achat : is the total sum of all Achat Direct Model (AchatDirectModel)
    #     """
    #     today = datetime.date.today()
    #     vente = db_vente.objects.filter(
    #         created_date__day=today.day)
    #     depot = db_depot.objects.filter(
    #         created_date__day=today.day)
    #     achat = db_achat.objects.filter(
    #         created_date__day=today.day)
            
    #     # sum_vente = sum(
    #     #     [p.price_total for p in vente if p.price_total != None])
    #     # sum_depot = sum(
    #     #     [p.produit.price_total for p in depot if p.produit.price_total != None])
    #     # sum_achat = sum(
    #     #     [p.produit.price_total for p in achat if p.produit.price_total != None])
    #     sales = sum(
    #         [p.price_total for p in vente if p.price_total != None])
    #     # context['benefice'] = self.benefice_vente(
    #     #     AchatDirectModel, DepotVenteModel, sales)
    #     return (sum_vente - (sum_depot + sum_achat))

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
        sum_vente = sum(
            [p.price_total for p in vente if p.price_total != None])
        sum_depot = sum(
            [p.produit.price_total for p in depot if p.produit.price_total != None])
        sum_achat = sum(
            [p.produit.price_total for p in achat if p.produit.price_total != None])
        return (sum_vente - (sum_depot + sum_achat))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        context = super().get_context_data(**kwargs)
        context['n_shops'] = Shop.objects.all().count()
        # context['benefice_day'] = self.benefice_per_day(
            # VenteModel, DepotVenteModel, AchatDirectModel)
        context['benefice_month'] = self.benefice_per_month(
            VenteModel, DepotVenteModel, AchatDirectModel)

        context["dataset_achat"] = self.chartObject(
            VenteModel, key='price_total', dt_col_name='created_date')
        context['dataset_depot'] = self.chartObject(
            ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date')
        context["dataset_stock"] = self.chartObject(
            ProductModel, key='price_total', dv_or_ad='AD', dt_col_name='created_date')
        if self.request.user.is_superuser:
            context["achat_directs"] = AchatDirectModel.objects.all().order_by(
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
        else:
            context["achat_directs"] = AchatDirectModel.objects.filter(
                produit__shop__owner__user__username=uname).order_by('-created_date')
            context["ventes"] = VenteModel.objects.filter(
                produit__shop__owner__user__username=uname).order_by('-created_date')
            context["tendance_vente"] = VenteModel.objects.filter(produit__shop__owner__user__username=uname).values(
                'produit__name').annotate(freq=Count('produit__name')).order_by()
            context["tendance_achat_direct"] = AchatDirectModel.objects.filter(
                produit__shop__owner__user__username=uname).values('produit__name').annotate(freq=Count('produit__name')).order_by()
            context["n_product"] = ProductModel.objects.filter(
                shop__owner__user__username=uname).count()
            context["n_client"] = ClientModel.objects.filter(
                shop__owner__user__username=uname).count()

        # Having the benefice

        return context


class ClientRequestView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):

    template_name = 'dashboard/client_request/client_request.html'
    model = ClientRequestModel
    fields = '__all__'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        uname = self.request.user.username
        context['achat_directs'] = self.q = AchatDirectModel.objects.all().order_by(
            '-created_date')
        context['count_item'] = self.q.count()
        context["tendance_achat_direct"] = AchatDirectModel.objects.values(
            'produit__name').annotate(freq=Count('produit__name')).order_by("?")
        context['spent'] = sum(
            [p.produit.price_total for p in self.q if p.produit.price_total != None])
        context['benefice'] = self.benefice_achat_direct(
            VenteModel, DepotVenteModel, context['spent'])

        if self.request.user.is_superuser:
            context["dataset_achat_direct"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='AD', dt_col_name='created_date')
        else:
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


class AchatDirectDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'dashboard/achat_direct/achat_direct_delete.html'
    model = AchatDirectModel


# First, creating the DepotVenteView
class DepotVenteView(LoginRequiredMixin, RedirectToPreviousMixin, TemplateView, Utils):
    template_name = 'dashboard/depot_vente/depot_vente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        self.q = DepotVenteModel.objects.order_by('-created_date')
        context["tendance_depot_vente"] = DepotVenteModel.objects.values(
            'produit__name').annotate(freq=Count('produit__name')).order_by("?")
        # Nombre de produit
        context['depot_ventes'] = self.q
        context['total_item'] = self.q.count()
        # Sum des produits de depots ventes
        context['spent_depot'] = sum(
            [p.produit.price_total for p in self.q if p.produit.price_total != None])
        # benefice
        context['benefice'] = self.benefice_depot_vente(
            AchatDirectModel, VenteModel, context['spent_depot'])
        if self.request.user.is_superuser:
            context['dataset_depot'] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date')
        else:
            context["dataset_depot"] = self.chartObject(
                ProductModel, key='price_total', dv_or_ad='DV', dt_col_name='created_date', uname=uname, is_superuser=False)
        return context


# Second, create the DepotVenteDetailView
class DepotVenteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/depot_vente/depot_vente_detail.html'
    model = DepotVenteModel
    context_object_name = 'd_vente'


# Third, create the depotVenteStockEditView
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
    form_class = VenteForm

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

        vente_qty = form.instance.quantity
        remaining_qty = product.quantity - vente_qty
        if remaining_qty < 0:
            messages.error(self.request, "Il ne reste que {} object(s) de {}".format(
                product.quantity, product.name))
        # elif remaining_qty == 0:
        #     ProductModel.objects.filter(pk=form.instance.produit.pk).delete()
        else:
            product.quantity = remaining_qty
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
        context['vente'] = self.q = VenteModel.objects.order_by(
            '-created_date')
        context["tendance_vente"] = VenteModel.objects.values(
            'produit__name').annotate(freq=Count('produit__name')).order_by("?")
        context['count_item'] = self.q.count()
        context['revenue'] = sales = sum(
            [p.price_total for p in self.q if p.price_total != None])
        context['benefice'] = self.benefice_vente(
            AchatDirectModel, DepotVenteModel, sales)

        uname = self.request.user.username
        if self.request.user.is_superuser:
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date')
        else:
            context["dataset_vente"] = self.chart_vente(
                VenteModel, key='price_total', dt_col_name='created_date', uname=uname, is_superuser=False)

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
    context_object_name = 'vente'


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
            shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Votre formulaire est incorrect!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uname = self.request.user.username
        if self.request.user.is_superuser:
            # What the superAdmin will see
            context['clients'] = self.c = ClientModel.objects.all()
            context['c_number'] = count = self.c.count()
            context["dataset_client"] = self.chart_client(
                ClientModel, key='passage', dt_col_name='created_date')
        else:
            # What the simpleAdmin sill see
            context['clients'] = ClientModel.objects.filter(
                shop__owner__user__username=uname)
            context["dataset_client"] = self.chart_client(
                ClientModel, key='passage', dt_col_name='created_date', uname=uname, is_superuser=False)

        # What both will see
        context['title'] = 'Espace Client'
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
    context_object_name = 'client'


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/client/client_detail.html'
    model = ClientModel
    context_object_name = 'client'

    def get_queryset(self):
        u_user = self.request.user
        if not u_user.is_superuser:
            self.client = ClientModel.objects.filter(pk=self.kwargs["pk"],
                                                     shop__owner__user__username=u_user.username)
        else:
            self.client = ClientModel.objects.filter(pk=self.kwargs["pk"])
        return self.client

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
    model = DevisModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:devisPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devis'] = self.a = DevisModel.objects.all()
        context['d_number'] = self.a.count()
        # context['f_number'] = self.a.count()
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
        context['v_product'] = self.q.product_name
        ################################################################

        return context


class EstimationPage(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/estimation/estimation.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:estimationPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estimates'] = self.e = EstimationModel.objects.all()
        return context


class EstimationResultPage(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/estimation/estimationResult.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:estimationPage')

    def estimation(self, db_estimation):
        my_estimation = db_estimation.objects.get(pk=self.kwargs["pk"])

        i_price = float(my_estimation.used_price)

        percentage_1 = 0
        if my_estimation.estate == 'NEUF':
            percentage_1 = 0
        elif my_estimation.estate == 'BON':
            percentage_1 = 0.05
        elif my_estimation.estate == 'MOYEN':
            percentage_1 = 0.1
        elif my_estimation.estate == 'MAUVAIS':
            percentage_1 = 0.2
        else:
            percentage_1 = None

        i_price = i_price - i_price * percentage_1
        percentage_2 = 0
        if my_estimation.obsolescence == 'LENTE':
            percentage_2 = 0
        elif my_estimation.obsolescence == 'MOYENNE':
            percentage_2 = 0.05
        elif my_estimation.obsolescence == 'RAPIDE':
            percentage_2 = 0.1
        elif my_estimation.obsolescence == 'TRES_RAPIDE':
            percentage_2 = 0.2
        else:
            percentage_2 = None
        i_price = i_price - i_price * percentage_2

        percentage_3 = 0
        if my_estimation.rarety == 'RARE':
            percentage_3 = 0
        elif my_estimation.rarety == 'COURANT':
            percentage_3 = 0.05
        elif my_estimation.rarety == 'TRES_COURANT':
            percentage_3 = 0.1
        else:
            percentage_3 = None

        i_price = i_price - i_price * percentage_3

        percentage_4 = 0
        if my_estimation.original_box == True:
            percentage_4 = 0
        else:
            percentage_4 = 0.05

        i_price = i_price - i_price * percentage_4

        percentage_5 = 0
        if my_estimation.charger == 'OUI':
            percentage_5 = 0
        elif my_estimation.charger == 'NON':
            percentage_5 = 0.05
        elif my_estimation.charger == 'PAS_BESOIN':
            percentage_5 = 0
        else:
            percentage_5 = 0
        i_price = i_price - i_price * percentage_5

        percentage_6 = 0
        if my_estimation.sale_bill == True:
            percentage_6 = 0
        else:
            percentage_6 = 0.05
        i_price = i_price - i_price * percentage_6

        percentage_7 = 0
        if my_estimation.dimension == 'PETIT':
            percentage_7 = 0
        elif my_estimation.dimension == 'MOYEN':
            percentage_7 = 0.05
        elif my_estimation.dimension == 'GRAND':
            percentage_7 = 0.1
        else:
            percentage_7 = None
        i_price = i_price - i_price * percentage_7

        return int(i_price)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_devis'] = self.a = EstimationModel.objects.all()
        context['e_number'] = self.a.count()
        context['estimates'] = self.q = EstimationModel.objects.get(
            pk=self.kwargs["pk"])
        context['estimation_result'] = self.estimation(EstimationModel)
        context['c_fname'] = self.q.client_name
        context['c_address'] = self.q.address
        context['c_tel'] = self.q.numero
        context['v_date'] = date = self.q.created_date
        date = date.strftime("%B-%d")
        context['v_date'] = date
        context['v_product'] = self.q.product_name
        return context
    



class EstimationDeletePage(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    template_name = 'dashboard/estimation/estimationDelete.html'
    model = EstimationModel
    context_object_name = 'estimates'
