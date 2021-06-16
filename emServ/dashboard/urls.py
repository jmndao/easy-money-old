from django.urls import path
import dashboard.views as d_views

app_name = 'dashboard'


urlpatterns = [

    path('', d_views.IndexView.as_view(), name="homePage"),
    # Client Routers
    path('client/', d_views.ClientView.as_view(), name="clientPage"),
    path('client/modifier/<int:pk>/', d_views.ClientUpdateView.as_view(), name='clientEditPage'),
    path('client/supprimer/<int:pk>/', d_views.ClientDeleteView.as_view(), name='clientDeletePage'),
    path('client/detail/<int:pk>/', d_views.ClientDetailView.as_view(), name='clientDetailPage'),
    # ClientRequest Routers
    path('demande_client/', d_views.ClientRequestView.as_view(), name="clientRequestPage"),
    path('demande_client/modifier/<int:pk>/', d_views.ClientRequestUpdateView.as_view(), name='clientRequestEditPage'),
    path('demande_client/detail/<int:pk>/', d_views.ClientRequestDetailView.as_view(), name='clientRequestDetailPage'),
    # Achat Direct Routers
    path('achat_direct/', d_views.AchatDirectView.as_view(), name="depositStockPage"),
    path('achat_direct/modifier/<int:pk>/', d_views.AchatDirectUpdateView.as_view(), name='achatDirectEditPage'),
    path('achat_direct/supprimer/<int:pk>/', d_views.AchatDirectDeleteView.as_view(), name='achatDirectDeletePage'),
    path('achat_direct/detail/<int:pk>/', d_views.AchatDirectDetailView.as_view(), name='achatDirectDetailPage'),
    # DepotVenteStock Routers
    path('depot_vente/', d_views.DepotVenteStockView.as_view(), name = 'depotVentePage'),
    # BuyingStock Routers
    path('vente/', d_views.BuyingStockView.as_view(), name="ventePage"),
    path('vente/modifier/<int:pk>/', d_views.VenteUpdateView.as_view(), name='venteEditPage'),
    path('vente/supprimer/<int:pk>/', d_views.VenteDeleteView.as_view(), name='venteDeletePage'),
    path('vente/detail/<int:pk>/', d_views.VenteDetailView.as_view(), name='venteDetailPage'),
    # Product Routers
    path('produit/', d_views.ProductView.as_view(), name="productPage"),
    path('produit/modifier/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('produit/supprimer/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    path('produit/detail/<int:pk>/', d_views.ProductDetailView.as_view(), name='productDetailPage'),
    # Profile Router
    # path('profile/', d_views.ProfileView.as_view(), name="profilePage"),
    
]
