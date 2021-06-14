from django.urls import path
import accounts.views as a_views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    # Profile Routers
    path('profile/', a_views.UserProfileView.as_view(), name='profilePage'),
    path('profile_edit/<int:pk>/', a_views.user_edit, name='profileEditPage'),
    path('profile_delete/<int:pk>/', a_views.UserProfileDeleteView.as_view(), name='profileDeletePage'),
    path('profile_detail/<int:pk>/', a_views.UserProfileDetailView.as_view(), name='profileDetailPage'),
    # Accounts Routers
    path('login/', a_views.AppLoginView.as_view(), name='loginPage'),
    path('register/', a_views.AppRegisterView.as_view(), name='registerPage'),
    path('logout/', LogoutView.as_view(next_page='accounts:loginPage'), name='logoutPage')
]
