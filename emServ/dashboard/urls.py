from django.urls import path
import dashboard.views as d_views

app_name = 'dashboard'


urlpatterns = [

    path('', d_views.IndexView.as_view(), name="homePage"),
    # Client Routers
    path('client/', d_views.ClientView.as_view(), name="clientPage"),
    path('client_edit/<int:pk>/', d_views.ClientUpdateView.as_view(), name='clientEditPage'),
    path('client_delete/<int:pk>/', d_views.ClientDeleteView.as_view(), name='clientDeletePage'),
    path('client_detail/<int:pk>/', d_views.ClientDetailView.as_view(), name='clientDetailPage'),
    # ClientRequest Routers
    path('client_request/', d_views.ClientRequestView.as_view(), name="clientRequestPage"),
    path('client_request_edit/<int:pk>/', d_views.ClientRequestUpdateView.as_view(), name='clientRequestEditPage'),
    path('client_request_delete/<int:pk>/', d_views.ClientRequestDeleteView.as_view(), name='clientRequestDeletePage'),
    path('client_request_detail/<int:pk>/', d_views.ClientRequestDetailView.as_view(), name='clientRequestDetailPage'),
    # DepositStock Routers
    path('deposit_stock/', d_views.DepositStockView.as_view(), name="depositStockPage"),
    path('deposit_stock_edit/<int:pk>/', d_views.DepositStockUpdateView.as_view(), name='depositStockEditPage'),
    path('deposit_stock_delete/<int:pk>/', d_views.DepositStockDeleteView.as_view(), name='depositStockDeletePage'),
    path('deposit_stock_detail/<int:pk>/', d_views.DepositStockDetailView.as_view(), name='depositStockDetailPage'),
    # DepotVenteStock Routers
    path('depot_vente_stock/', d_views.DepotVenteStockView.as_view(), name = 'depotVenteStockPage'),



    # BuyingStock Routers
    path('buying_stock/', d_views.BuyingStockView.as_view(), name="buyingStockPage"),
    path('buying_stock_edit/<int:pk>/', d_views.BuyingStockUpdateView.as_view(), name='buyingStockEditPage'),
    path('buying_stock_delete/<int:pk>/', d_views.BuyingStockDeleteView.as_view(), name='buyingStockDeletePage'),
    path('buying_stock_detail/<int:pk>/', d_views.BuyingStockDetailView.as_view(), name='buyingStockDetailPage'),
    # Product Routers
    path('product/', d_views.ProductView.as_view(), name="productPage"),
    path('product_edit/<int:pk>/', d_views.ProductUpdateView.as_view(), name='productEditPage'),
    path('product_delete/<int:pk>/', d_views.ProductDeleteView.as_view(), name='productDeletePage'),
    path('product_detail/<int:pk>/', d_views.ProductDetailView.as_view(), name='productDetailPage'),
    # Profile Router
    # path('profile/', d_views.ProfileView.as_view(), name="profilePage"),
    
]
