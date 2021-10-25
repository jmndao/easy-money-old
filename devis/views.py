from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models.functions import TruncDay
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from dashboard.utils import RedirectToPreviousMixin
from devis.models import DevisModel
from devis.forms import DevisModelForm
from dashboard.models import Shop
from clients.models import ClientModel

# Create your views here.


class GenerateDevis(LoginRequiredMixin, CreateView):
    template_name = 'devis/devis.html'
    form_class = DevisModelForm
    success_url = reverse_lazy('devis:devisPage')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Devis"
        user = self.request.user
        if user.is_superuser:
            context['devis'] = self.a =  DevisModel.objects.annotate(c_date=TruncDay('created_date')).values(
                'c_date', 'client__fname', 'client__lname', 'client__pk').annotate(c=Count('id'), total=Sum('price_total')).order_by()
        else:
            context['all_devis'] = self.a =  DevisModel.objects.filter(
                shop__owner__user=user).annotate(c_date=TruncDay('created_date')).values(
                'c_date', 'client__fname', 'client__lname', 'client__pk').annotate(c=Count('id'), total=Sum('price_total')).order_by()
        context['d_number'] = self.a.count() 
        return context


class DevisDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):
    template_name = 'devis/devisDelete.html'
    model = DevisModel
    context_object_name = 'devis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression - Devis"
        return context

class DevisDetailView(LoginRequiredMixin, DetailView):

    template_name = 'devis/devis_detail.html'
    model = DevisModel
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Devis"
        
        context["all_devis"] = DevisModel.objects.filter(
            client__pk=self.kwargs["pk"]
        )
        context["client"] = ClientModel.objects.get(pk=self.kwargs["pk"])
        return context  


class TirerDevis(LoginRequiredMixin, CreateView):
    template_name = 'devis/tirerDevis.html'
    model = DevisModel
    fields = '__all__'
    success_url = reverse_lazy('devis:devisPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['all_devis'] = self.a = DevisModel.objects.all()
        
        context['f_number'] = self.kwargs["pk"]
        
        devis = DevisModel.objects.filter(
            client__pk=self.kwargs["pk"], 
            created_date__day=self.kwargs["day"],
            created_date__month=self.kwargs["month"],
            created_date__year=self.kwargs["year"],
        )

        context["all_devis"] = devis
        context["d"] = devis[0] 
        context["total_price"] = sum(
            [d.price_total for d in devis if d.price_total])

        context['quantity'] = sum([qty.quantity for qty in devis])
        return context


class DevisUpdateView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):

    template_name = 'devis/devis_edit.html'
    model = DevisModel
    fields = '__all__'
    success_url = reverse_lazy('devis:devisPage')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Devis"
        return context

