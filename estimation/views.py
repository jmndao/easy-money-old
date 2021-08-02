from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import DetailView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from django.contrib.auth import login
from estimation.models import EstimationModel
from estimation.utils import Utils

# Create your views here.


class EstimationView(LoginRequiredMixin, CreateView, Utils):
    template_name = 'estimation/estimation.html'
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


# I have to work on this
def change_value(request):
    template_name = 'estimation/estimation.html'
    if request.method == 'POST':
        print('request is post')
    return render(request, template_name)


class LastEstimationPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'estimation/lastEstimation.html'
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
    template_name = 'estimation/estimation_detail.html'
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
    template_name = 'estimation/estimationEdit.html'
    fields = '__all__'
    model = EstimationModel
    success_url = reverse_lazy('estimation:estimationPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EstimationResultPage(LoginRequiredMixin, CreateView, Utils):
    template_name = 'estimation/estimationResult.html'
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
    template_name = 'estimation/estimationDelete.html'
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


# Error handling
def error_404(request, exception):
    data = {}
    return render(request, 'myerrors/404.html', data)


def error_500(request):
    data = {}
    template_name = 'dashboard/myerrors/500.html'
    return render(request, template_name, data)
