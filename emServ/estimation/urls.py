from django.urls import path
import accounts.views as a_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
import estimation.views as e_views

from django.conf import settings
from django.conf.urls.static import static

from django.urls import reverse_lazy


app_name = 'estimation'

urlpatterns = [
    # Profile Routers
    path('', e_views.EstimationView.as_view(), name='estimationPage'),
    # path('estimation/delete/<int:pk>/', a_views.EstimationDeleteView.as_view(), name='estimationDeletePage'),
    path('resultat/<int:pk>/', e_views.EstimationResultPage.as_view(),
         name='estimationResultPage'),
    path('supprimer/<int:pk>/', e_views.EstimationDeletePage.as_view(),
         name='estimationDeletePage'),
    path('dernier/', e_views.LastEstimationPage.as_view(),
         name='lastEstimationPage'),
    path('supprimer_plusieur/', e_views.multiple_delete_estimation,
         name='multipleDeleteEstimationPage'),
    path('detail/<int:pk>/', e_views.EstimationDetail.as_view(),
         name='estimationDetailPage'),
    path('modifier/<int:pk>/', e_views.EstimationEdit.as_view(),
         name='estimationEditPage'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
