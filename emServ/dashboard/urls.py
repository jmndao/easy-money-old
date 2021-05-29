
from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [

    path('', views.index, name="homePage"),
    path('client/', views.client, name="clientPage"),
    path('demande_client/', views.clientRequest, name='clientRequestPage'),
    path('stock_depot/', views.depositStock, name="depositStockPage"),
    path('stock_achat/', views.buyingStock, name="buyingStockPage"),
    path('profile/', views.profile, name="profilePage"),
    path('produit/', views.product, name="productPage")
    
]
