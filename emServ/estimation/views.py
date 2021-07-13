from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.views.generic import (TemplateView,
                                  DetailView,
                                  ListView)
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                       )
from django.contrib.auth import login
from estimation.models import EstimationModel
from estimation.utils import Utils

# Create your views here.


class EstimationView(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/estimation.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('estimation:lastEstimationPage')

    def form_valid(self, form):
        form.instance.final_price = self.estimation_from_form(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Estimation"
        user = self.request.user
        if user.is_superuser:
            context['estimates'] = self.e = EstimationModel.objects.all()
        else:
            context['estimates'] = self.e = EstimationModel.objects.filter(
                shop__owner__user=user)
        return context


class LastEstimationPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/lastEstimation.html'
    model = EstimationModel
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estimates'] = self.q = EstimationModel.objects.last()
        context['estimation_result'] = self.estimation_from_model(
            EstimationModel, last=True)
        context['new_price'] = self.q.new_price
        context['name_product'] = self.q.product_name
        context['reparation'] = self.q.reparatinon_price
        return context


class EstimationDetail(LoginRequiredMixin, DetailView):
    model = EstimationModel
    template_name = 'dashboard/estimation/estimation_detail.html'
    context_object_name = 'estimation'

    def get_queryset(self):
        u_user = self.request.user
        if not u_user.is_superuser:
            self.estimation = EstimationModel.objects.filter(pk=self.kwargs["pk"],
                                                             shop__owner__user__username=u_user.username)
        else:
            self.estimation = EstimationModel.objects.filter(
                pk=self.kwargs["pk"])
        return self.estimation


class EstimationEdit(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/estimation/estimationEdit.html'
    fields = '__all__'
    model = EstimationModel
    success_url = reverse_lazy('dashboard:estimationPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EstimationResultPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'dashboard/estimation/estimationResult.html'
    model = EstimationModel
    fields = '__all__'
    success_url = reverse_lazy('estimation:estimationPage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_devis'] = self.a = EstimationModel.objects.all()
        context['e_number'] = self.a.count()
        context['estimates'] = self.q = EstimationModel.objects.get(
            pk=self.kwargs["pk"])
        context['estimation_result'] = self.estimation_from_model(
            EstimationModel, last=False, pk=self.kwargs["pk"])
        context['c_fname'] = self.q.seller
        context['c_address'] = self.q.address
        context['c_tel'] = self.q.numero
        context['v_date'] = date = self.q.created_date
        date = date.strftime("%B-%d")
        context['v_date'] = date
        context['v_product'] = self.q.product_name
        return context


class EstimationDeletePage(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/estimation/estimationDelete.html'
    model = EstimationModel
    context_object_name = 'estimates'

# Delete Multiple Estimation


def multiple_delete_estimation(request):
    if request.method == 'POST':
        estimate_ids = request.POST.getlist('id[]')
        for id in estimate_ids:
            estimate = EstimationModel.objects.get(pk=id)
            estimate.delete()
    return redirect('dashboard:homePage')
