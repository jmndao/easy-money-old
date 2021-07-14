from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from dashboard.utils import RedirectToPreviousMixin
from devis.models import DevisModel
from ventes.models import VenteModel
from devis.forms import DevisModelForm

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
            context['devis'] = self.a = DevisModel.objects.all()
            context['d_number'] = self.a.count() 
        else:
            context['devis'] = self.a = DevisModel.objects.filter(shop__owner__user=user)
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
    


class TirerDevis(LoginRequiredMixin, CreateView):
    template_name = 'devis/tirerDevis.html'
    model = VenteModel
    fields = '__all__'
    success_url = reverse_lazy('devis:devisPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_devis'] = self.a = DevisModel.objects.all()
        context['f_number'] = self.a.count()
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
        context['v_product'] = self.q.produit.name
        return context
