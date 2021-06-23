from django.urls import path
import accounts.views as a_views
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static


app_name = 'accounts'

urlpatterns = [
    # Profile Routers
    path('profile/', a_views.UserProfileCreationView.as_view(), name='profilePage'),
    path('profile/editer/<int:pk>/', a_views.UserProfileUpdateView.as_view(), name='profileUpdatePage'),
    # User Routers
    path('agent/nouveau/', a_views.UserCreationView.as_view(), name='userCreationPage'),
    path('agent/modifier/<int:pk>/', a_views.UserUpdateView.as_view(), name='userUpdatePage'),
    path('agent/delete/<int:pk>/', a_views.UserDeleteView.as_view(), name='userDeletePage'),
    # Shop Routers
    path('boutique/nouveau/', a_views.ShopCreationView.as_view(), name='shopCreationPage'),
    path('boutique/modifier/<int:pk>/', a_views.ShopUpdateView.as_view(), name='shopUpdatePage'),
    # Accounts Routers
    path('login/', a_views.AppLoginView.as_view(), name='loginPage'),
    path('register/', a_views.AppRegisterView.as_view(), name='registerPage'),
    path('logout/', LogoutView.as_view(next_page='accounts:loginPage'), name='logoutPage')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
