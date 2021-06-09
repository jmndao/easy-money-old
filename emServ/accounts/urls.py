from django.urls import path
import accounts.views as a_views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', a_views.AppLoginView.as_view(), name='loginPage'),
    path('register/', a_views.AppRegisterView.as_view(), name='registerPage'),
    path('logout/', LogoutView.as_view(next_page='accounts:loginPage'), name='logoutPage')
]
