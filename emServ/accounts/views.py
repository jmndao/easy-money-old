from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.contrib.auth import login

from accounts.models import UserProfile
from dashboard.models import Shop



class UserCreationView(LoginRequiredMixin, CreateView):

    form_class = UserCreationForm
    template_name = 'dashboard/users/user_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Agent {} a ete ajoute avec succes !".format(form.instance.username))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Un agent existe avec ce nom d'utilisateur !")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profileUpdatePage', args=(self.request.user.pk,))
    


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('accounts:profileUpdatePage')
    template_name = 'dashboard/users/user_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Vos modifications ont ete accepte !') 
        return super().form_valid(form)

    

class UserDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    template_name = 'accounts/users/user_delete.html'
    success_url = reverse_lazy('accounts:userCreationPage')



class UserProfileCreationView(LoginRequiredMixin, CreateView):

    model = UserProfile
    success_url = reverse_lazy('accounts:profileUpdatePage')
    template_name = 'dashboard/users/profile.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class UserProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = UserProfile
    success_url = reverse_lazy('accounts:profileUpdatePage')
    template_name = 'dashboard/users/profile.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["n_users"] = context["users"].count()
        return context



class ShopCreationView(LoginRequiredMixin, CreateView):

    model = Shop
    fields = '__all__'
    success_url = reverse_lazy('accounts:profilePage')
    template_name = 'dashboard/shop/shop_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()
        context["n_shop"] = context["shops"].count()
        return context



class ShopUpdateView(LoginRequiredMixin, UpdateView):

    model = Shop
    fields = '__all__'
    success_url = reverse_lazy('accounts:shopCreationPage')
    template_name = 'accounts/shop/shop_update.html'
        


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

