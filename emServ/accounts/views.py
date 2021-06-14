from django.db.models import fields
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.urls.base import reverse
from django.views.generic import DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from django.forms.models import inlineformset_factory


from accounts.forms import UserForm
from accounts.models import UserProfile


@login_required()
def user_edit(request, pk):

    user = User.objects.get(pk=pk)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields='__all__', extra=0)
    user_form = UserForm(instance=user)
    formset = ProfileInlineFormset(instance=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                return HttpResponseRedirect(reverse('accounts:profilePage', args=[pk]))

    context = {
        'pk' : pk,
        'user_form' : user_form,
        'formset' : formset
    }

    return render(request, 'dashboard/users/user_edit.html', context)


class UserProfileView(LoginRequiredMixin, CreateView):

    model = UserProfile
    success_url = reverse_lazy('dashboard:homePage')
    template_name = 'dashboard/users/user.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["me"] = User.objects.get(username=self.request.user.username)
        return context
    
    

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    
    model = User
    success_url = reverse_lazy('accounts:profileUpdatePage')
    context_object_name = 'profile'
    template_name = 'dashboard/users/user_delete.html'


class UserProfileDetailView(LoginRequiredMixin, DetailView):

    model = UserProfile
    context_object_name = 'profile'
    template_name = 'dashboard/users/user_detail.html'


class AppLoginView(LoginView):

    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:homePage')


class AppRegisterView(FormView):

    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    redirect_to_login = True
    success_url = reverse_lazy('accounts:loginPage')

    def form_valid(self, form):

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard:homePage')
        return super().get(*args, **kwargs)

