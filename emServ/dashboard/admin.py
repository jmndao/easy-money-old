from django.contrib import admin

# Register your models here.
from dashboard.models import (
    ProductModel,
    AchatDirectModel,
    VenteModel,
    ClientRequestModel,
    DepotVenteModel,
    Shop
)

admin.site.register(ProductModel)
admin.site.register(AchatDirectModel)
admin.site.register(VenteModel)
admin.site.register(ClientRequestModel)
admin.site.register(DepotVenteModel)
admin.site.register(Shop)

