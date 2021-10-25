from django.urls import path
import devis.views as d_views

app_name = 'devis'

urlpatterns = [
    #Handling the devis page
    path('details-devis/<int:pk>/', d_views.DevisDetailView.as_view(), name='devisDetailPage'),
    path('', d_views.GenerateDevis.as_view(), name = 'devisPage'),
    path('modifier/<int:pk>/', d_views.DevisUpdateView.as_view(), name='devisEditPage'),
    path('supprimer/<int:pk>/', d_views.DevisDeleteView.as_view(), name = 'devisDeletePage'),
    path('tirer/<int:pk>/<int:day>/<int:month>/<int:year>/', d_views.TirerDevis.as_view(), name = 'tirerDevisPage'),
]
