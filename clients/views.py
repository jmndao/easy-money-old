from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.utils import RedirectToPreviousMixin, Utils
from dashboard.models import Shop
from clients.models import ClientModel
from ventes.models import VenteModel

from templated_email import send_templated_mail
from django.conf import settings
# Create your views here.


class ClientView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView, Utils):

    template_name = 'clients/clients.html'
    model = ClientModel
    fields = '__all__'
    success_url = reverse_lazy('clients:clientPage')

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

    template_name = 'clients/clients_edit.html'
    fields = '__all__'
    model = ClientModel

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            shop_owner = Shop.objects.get(
                owner__user__username=self.request.user.username)
            form.instance.shop = shop_owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Espace Client"
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'clients/clients_detail.html'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Espace Client"
        context["ventes_client"] = vs = VenteModel.objects.filter(client=self.client[0])
        context["sum_ventes"] = sum([v.price_total for v in vs])
        return context

def send_invoice(request, pk):

    client = ClientModel.objects.get(pk=pk)
    
    if client.email:
        # Pick the latest sales made by the client
        lastest_passage = VenteModel.objects.filter(client=client).order_by('-created_date')[0].created_date.day
        ventes = VenteModel.objects.filter(client=client, created_date__day=lastest_passage)
        # Calculate the total sum
        total_price = sum([v.price_total for v in ventes if v.price_total])
        
        send_templated_mail(
                    template_name='invoice',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    context={
                        'ventes': ventes,
                        'total_price': total_price
                    }
                )
        messages.success(request, "La facture a été envoyé avec success à l'adresse {}".format(client.email))
        
        return redirect(reverse('clients:clientPage'))


    return render(request, 'clients/clients.html', context=None)


# Delete Multiple Client


def multiple_delete_client(request):
    if request.method == 'POST':
        client_ids = request.POST.getlist('id[]')
        for id in client_ids:
            client = ClientModel.objects.get(pk=id)
            client.delete()
    return redirect('clients:clientPage')
