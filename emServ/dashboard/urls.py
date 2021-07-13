from django.urls import path
import dashboard.views as d_views
from .views import DepotVenteDeleteView, DepotVenteDetailView, DepotVenteEditView, GeneratePDF

app_name = 'dashboard'


urlpatterns = [
    # For handling bills
    path('invoice/<int:pk>/', d_views.GeneratePDF.as_view(), name = 'invoice'),
    #Handling the devis page
    path('devis/', d_views.GenerateDevis.as_view(), name = 'devisPage'),
    path('devis/supprimer/<int:pk>/', d_views.DevisDeleteView.as_view(), name = 'devisDeletePage'),
    path('devis/tirer/<int:pk>/', d_views.TirerDevis.as_view(), name = 'tirerDevisPage'),
    #Handling the estimation page
    #Everything is now on the estimation app
    
    
    #This is the home page
    path('', d_views.IndexView.as_view(), name="homePage"),
    # Client Routers
    path('client/', d_views.ClientView.as_view(), name="clientPage"),
    path('client/modifier/<int:pk>/', d_views.ClientUpdateView.as_view(), name='clientEditPage'),
    path('client/supprimer/<int:pk>/', d_views.ClientDeleteView.as_view(), name='clientDeletePage'),
    path('client/supprimer_plusieur/', d_views.multiple_delete_client, name='multipleDeleteClientPage'),
    path('client/detail/<int:pk>/', d_views.ClientDetailView.as_view(), name='clientDetailPage'),
    # ClientRequest Routers
    path('demande_cliant/', d_views.ClientRequestView.as_view(), name="clientRequestPage"),
    path('demande_cliant/modifier/<int:pk>/', d_views.ClientRequestUpdateView.as_view(), name='clientRequestEditPage'),
    path('demande_cliant/supprimer_plusieur/', d_views.multiple_delete_clientRequest, name='multipleDeleteClientRequestPage'),
    path('demande_cliant/detail/<int:pk>/', d_views.ClientRequestDetailView.as_view(), name='clientRequestDetailPage'),
    # Achat Direct Routers
    path('achat_direct/', d_views.AchatDirectView.as_view(), name="achatDirectPage"),
    path('achat_direct/modifier/<int:pk>/', d_views.AchatDirectUpdateView.as_view(), name='achatDirectEditPage'),
    path('achat_direct/supprimer/<int:pk>/', d_views.AchatDirectDeleteView.as_view(), name='achatDirectDeletePage'),
    path('achat_direct/supprimer_plusieur/', d_views.multiple_delete_achatDirect, name='multipleDeleteAchatDirectPage'),
    path('achat_direct/detail/<int:pk>/', d_views.AchatDirectDetailView.as_view(), name='achatDirectDetailPage'),
    # DepotVenteStock Routers
    path('depot_vent/', d_views.DepotVenteView.as_view(), name = 'depotVentePage'),
    path('depot_vent/detail/<int:pk>/', d_views.DepotVenteDetailView.as_view(), name='depotVenteDetailPage'),
    path('depot_vent/supprimer/<int:pk>/', d_views.DepotVenteDeleteView.as_view(), name='depotVenteDeletePage'),
    path('depot_vent/supprimer_plusieur/', d_views.multiple_delete_depotVente, name='multipleDeleteDepotVentePage'),
    path('depot_vent/modifier/<int:pk>/', d_views.DepotVenteEditView.as_view(), name='depotVenteEditPage'),
    # BuyingStock Routers
    path('vente/', d_views.VenteView.as_view(), name="ventePage"),
    path('vente/modifier/<int:pk>/', d_views.VenteUpdateView.as_view(), name='venteEditPage'),
    path('vente/supprimer/<int:pk>/', d_views.VenteDeleteView.as_view(), name='venteDeletePage'),
    path('vente/supprimer_plusieur/', d_views.multiple_delete_vente, name='multipleDeleteVentePage'),
    path('vente/detail/<int:pk>/', d_views.VenteDetailView.as_view(), name='venteDetailPage'),
    # Product Routers
    path('produit/', d_views.ProductView.as_view(), name="productPage"),
    path('produit/modifier/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('produit/supprimer/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    path('product/supprimer_plusieur/', d_views.multiple_delete_product, name='multipleDeleteProductPage'),
    path('produit/detail/<int:pk>/', d_views.ProductDetailView.as_view(), name='productDetailPage'),
    # Profile Router
    # path('profile/', d_views.ProfileView.as_view(), name="profilePage"),
    
]
