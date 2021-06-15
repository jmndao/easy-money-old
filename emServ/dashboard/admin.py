from django.contrib import admin

# Register your models here.
from dashboard.models import (
    ProductModel,
    DepositStockModel,
    BuyingStockModel,
    ClientModel,
    ClientRequestModel,
    DepotVenteStockModel,
    Shop
)

admin.site.register(ProductModel)
admin.site.register(DepositStockModel)
admin.site.register(BuyingStockModel)
admin.site.register(ClientRequestModel)
admin.site.register(ClientModel)
admin.site.register(DepotVenteStockModel)
admin.site.register(Shop)

