from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from dashboard.utils import RedirectToPreviousMixin
from dashboard.models import Shop
from clientRequests.models import ClientRequestModel

# Create your views here.


class ClientRequestView(LoginRequiredMixin, CreateView):

    template_name = 'clientRequests/client_request.html'
    model = ClientRequestModel
    fields = '__all__'
    success_url = reverse_lazy('clientRequests:clientRequestPage')
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Demande Client"
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

    template_name = 'clientRequests/client_request_edit.html'
    model = ClientRequestModel
    fields = '__all__'
    success_url = reverse_lazy('clientRequests:clientRequestPage')

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.shop = Shop.objects.get(
                owner__user__username=self.request.user.username)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Demande Utilisateur"
        return context
    


class ClientRequestDetailView(LoginRequiredMixin, DetailView):

    template_name = 'clientRequests/client_request_detail.html'
    model = ClientRequestModel

    def get_queryset(self):
        uname = self.request.user.username
        self.client_request = get_object_or_404(ClientRequestModel,
                                                pk=self.kwargs['pk'],
                                                client__shop__owner__user__username=uname)
        return self.client_request
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail-Demande Utilisateur"
        return context
    


class ClientRequestDeleteView(LoginRequiredMixin, RedirectToPreviousMixin, DeleteView):

    template_name = 'clientRequests/client_request_delete.html'
    model = ClientRequestModel
    success_url = reverse_lazy('clientRequests:clientRequestPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression-Demande Utilisateur"
        return context

#Delete Multiple Delete ClientRequest
def multiple_delete_clientRequest(request):
    if request.method == 'POST':
        c_req_ids = request.POST.getlist('id[]')
        for id in c_req_ids:
            c_req = ClientRequestModel.objects.get(pk=id)
            c_req.delete()
    return redirect('clientRequests:clientRequestPage')
