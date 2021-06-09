from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, redirect_to_login
from django.views.generic.edit import FormView
from accounts.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


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

