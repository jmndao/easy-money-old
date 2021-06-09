from django.urls import path
import dashboard.views as d_views

app_name = 'dashboard'


urlpatterns = [

    path('', d_views.IndexView.as_view(), name="homePage"),
    # Client Routers
    path('client/', d_views.ClientView.as_view(), name="clientPage"),
    # path('client_edit/<int:pk>/', d_views.ClientUpdateView.as_view(), name='clientEditPage'),
    # path('client_delete/<int:pk>/', d_views.ClientDeleteView.as_view(), name='clientDeletePage'),
    # path('client_detail/<int:pk>/', d_views.ClientDetailView.as_view(), name='clientDetailPage'),
    #
    path('demande_client/', d_views.clientRequest, name='clientRequestPage'),
    #
    # Product Routers
    path('product/', d_views.ProductView.as_view(), name="productPage"),
    path('product_edit/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('product_delete/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    path('product_detail/<int:pk>/', d_views.ProductDetailView.as_view(), name='productDetailPage'),
    #
    # Deposit Stock Routers
    path('stock_depot/', d_views.ProductDeposit.as_view(), name='depositStockPage'),
    # path('stock_depot/<int:pk>/', d_views.ProductDepositUpdateView.as_view(), name="depositStockEditPage"),
    # Buying Stock Routers
    path('stock_achat/', d_views.buyingStock, name="buyingStockPage"),
    # Profile Router
    path('profile/', d_views.profile, name="profilePage"),
    
]
