from django.urls import path
import accounts.views as a_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView

from django.conf import settings
from django.conf.urls.static import static

from django.urls import reverse_lazy

app_name = 'estimation'

urlpatterns = [
    # Profile Routers
    path('estimation/', a_views.EstimationView.as_view(), name='estimationPage'),
    path('estimation/delete/<int:pk>/', a_views.EstimationDeleteView.as_view(), name='estimationDeletePage'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
