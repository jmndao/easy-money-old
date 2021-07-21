from datetime import date
from django.conf import settings
from django.contrib.auth import get_user, login, logout
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from accounts.forms import PasswordForm, form_validation_error
from accounts.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import DeleteView, FormView, UpdateView

from dashboard.models import Shop
from accounts.forms import UserProfileForm
from accounts.resources import ProductExcel, VenteExcel, ClientExcel

history = {} 

class UserCreationView(LoginRequiredMixin, CreateView):

    form_class = UserCreationForm
    template_name = 'dashboard/users/user_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Agent {} a été ajouté avec succes !".format(form.instance.username))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Un agent existe avec ce nom d'utilisateur !")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profilePage')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creation-Utilisateur"
        return context
    

class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['username']
    template_name = 'dashboard/users/user_update.html'

    def form_valid(self, form):
        u_user = User.objects.get(pk=self.kwargs["pk"])
        messages.success(self.request, 'Modifications enregistré avec succès pour {}'.format(u_user)) 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profilePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_user = User.objects.get(pk=self.kwargs["pk"])
        context["title"] = "Modification-{}".format(u_user)
        return context
    
    
class UserDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    template_name = 'dashboard/users/user_delete.html'
    success_url = reverse_lazy('accounts:profilePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_user = User.objects.get(pk=self.kwargs["pk"])
        context["title"] = "Suppression-{}".format(u_user)
        return context

    def form_valid(self, form):
        u_user = User.objects.get(pk=self.kwargs["pk"])
        messages.success(self.request, "{} supprimé avec success.".format(u_user)) 
        return super().form_valid(form)
    

def change_password_view(request, pk):
    u_user = User.objects.get(pk=pk)

    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('ancient_pwd')
            if not u_user.check_password(old_password):
                messages.error(request, "L'ancien mot de passe ne correspond pas")
                return redirect(reverse('accounts:passwordChangePage', args=(pk,)))
            if form.cleaned_data.get('new_password') != form.cleaned_data.get('new_confirmation_password'):
                messages.error(request, "Vos mot de passe ne correspondent pas.")
                return redirect(reverse('accounts:passwordChangePage', args=(pk,)))
            u_user.set_password(form.cleaned_data.get('new_password'))
            u_user.save()
            messages.success(request, "Mot de Passe modifié avec succès pour {}.".format(u_user))
            return redirect(reverse('accounts:profilePage'))
    form = PasswordForm()
    context = {
        "form": form,
        "title": "Mot de Passe-{}".format(u_user)
    }
    return render(request, 'dashboard/users/password_change.html', context)
    


class UserProfileView(View, LoginRequiredMixin):
    userprofile = None 

    def dispatch(self, request, *args, **kwargs):
        self.userprofile, _ = UserProfile.objects.get_or_create(user=request.user)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        shops = Shop.objects.all()
        context = {
            'logged_in_users': history.get('logged_in_users', None) if history else [],
            'shops': shops,
            'userprofile': self.userprofile, 
            'segment': 'profile',
            'title': "Profile"
        }
        return render(request, 'dashboard/users/profile.html', context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=self.userprofile)
        if form.is_valid():
            userprofile = form.save()
            userprofile.user.first_name = form.cleaned_data.get('first_name')
            userprofile.user.last_name = form.cleaned_data.get('last_name')
            userprofile.user.email = form.cleaned_data.get('email')
            userprofile.user.save()
            messages.success(request, 'Profile enregistré avec succes !')
        else:
            messages.error(request, form_validation_error(form))

        return redirect(reverse('accounts:profilePage'))


class ShopCreationView(LoginRequiredMixin, CreateView):

    model = Shop
    fields = '__all__'
    template_name = 'dashboard/shop/shop_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()
        context["n_shop"] = context["shops"].count()
        context["title"] = "Creation-Boutique"
        return context

    def get_success_url(self):
        return reverse_lazy('accounts:profilePage')



class ShopUpdateView(LoginRequiredMixin, UpdateView):

    model = Shop
    fields = '__all__'
    success_url = reverse_lazy('accounts:shopCreationPage')
    template_name = 'accounts/shop/shop_update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profileUpdatePage', args=(self.request.user.shop_user_related.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modification-Boutique"
        return context
    

class AppLoginView(LoginView):

    users = []
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:homePage')

    def form_valid(self, form):
        self.users.append(form.cleaned_data.get('username'))
        try:
            history['logged_in_users'] = self.users
        except Exception as e:
            pass
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Se Connecter"
        return context


def applogout(request):
    l_user = get_user(request).username
    try:
        list_users = history.get('logged_in_users', None)
        list_users.remove(l_user)
        if len(list_users) == 0:
            del history['logged_in_users']
        else:
            history['logged_in_users'] = list_users
    except Exception as e:
        pass
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
    

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration"
        return context
    


def export_product_view(request):
    product_excel = ProductExcel()
    dataset = product_excel.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    today_date = str(date.today())
    filename = "produit_" + today_date + ".xls"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response
    
def export_vente_view(request):
    vente_excel = VenteExcel()
    dataset = vente_excel.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    today_date = str(date.today())
    filename = "vente_" + today_date + ".xls"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response

def export_client_view(request):
    client_excel = ClientExcel()
    dataset = client_excel.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    today_date = str(date.today())
    filename = "client_" + today_date + ".xls"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response

