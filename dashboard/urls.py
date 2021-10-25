from django.urls import path
import dashboard.views as d_views
from .views import DepotVenteDeleteView, DepotVenteDetailView, DepotVenteEditView, GeneratePDF

app_name = 'dashboard'


urlpatterns = [
    # For handling bills
    path('invoice/<int:pk>/<int:day>/<int:month>/<int:year>', d_views.GeneratePDF.as_view(), name = 'invoice'),
    #This is the home page
    path('', d_views.IndexView.as_view(), name="homePage"),
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
    # Product Routers
    path('produit/', d_views.ProductView.as_view(), name="productPage"),
    path('produit/modifier/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('produit/supprimer/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    path('product/supprimer_plusieur/', d_views.multiple_delete_product, name='multipleDeleteProductPage'),
    path('produit/detail/<int:pk>/', d_views.ProductDetailView.as_view(), name='productDetailPage'),
    # Profile Router
    # path('profile/', d_views.ProfileView.as_view(), name="profilePage"),
    
]
