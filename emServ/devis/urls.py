from django.urls import path
import devis.views as d_views

urlpatterns = [
    #Handling the devis page
    path('', d_views.GenerateDevis.as_view(), name = 'devisPage'),
    path('supprimer/<int:pk>/', d_views.DevisDeleteView.as_view(), name = 'devisDeletePage'),
    path('tirer/<int:pk>/', d_views.TirerDevis.as_view(), name = 'tirerDevisPage'),
]
