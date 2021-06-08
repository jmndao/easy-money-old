
from django.urls import path
import dashboard.views as d_views

app_name = 'dashboard'


urlpatterns = [

    path('', d_views.IndexView.as_view(), name="homePage"),
    path('client/', d_views.ClientView.as_view(), name="clientPage"),
    path('demande_client/', d_views.clientRequest, name='clientRequestPage'),
    # Product Routers
    path('product_edit/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('product_delete/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    # Deposit Stock Routers
    path('stock_depot/', d_views.ProductDeposit.as_view(), name='depositStockPage'),
    #path('stock_depot/<int:pk>/', d_views.ProductDepositUpdateView.as_view(), name="depositStockEditPage"),
    # Buying Stock Routers
    path('stock_achat/', d_views.buyingStock, name="buyingStockPage"),
    # Profile Router
    path('profile/', d_views.profile, name="profilePage"),

    path('produit/', d_views.product, name="productPage")
    
]
