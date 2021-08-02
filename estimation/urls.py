from django.urls import path
import estimation.views as e_views

app_name = 'estimation'

urlpatterns = [
    # Estimation Routers
    path('', e_views.EstimationView.as_view(), name='estimationPage'),
    # I did add this url
    path('changer-valeur', e_views.change_value, name='change_value'),
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

]
