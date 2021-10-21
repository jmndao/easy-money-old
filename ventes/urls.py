from django.urls import path
import ventes.views as v_views

app_name = 'ventes'

urlpatterns = [
    # Vente Routers
    path('', v_views.VenteView.as_view(), name="ventePage"),
    path('facturer/<int:pk>/', v_views.multiple_vente_creation_view, name="venteCreationPage"),
    path('modifier/<int:pk>/', v_views.VenteUpdateView.as_view(), name='venteEditPage'),
    path('supprimer/<int:pk>/', v_views.VenteDeleteView.as_view(), name='venteDeletePage'),
    path('supprimer_plusieur/', v_views.multiple_delete_vente, name='multipleDeleteVentePage'),
    path('detail/<int:pk>/', v_views.VenteDetailView.as_view(), name='venteDetailPage'),
]
