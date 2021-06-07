from django.contrib import admin

# Register your models here.
from .models import ProductModel
from .models import DepositStockModel
from .models import BuyingStockModel
from .models import ClientRequestModel
from .models import ClientModel

admin.site.register(ProductModel)
admin.site.register(DepositStockModel)
admin.site.register(BuyingStockModel)
admin.site.register(ClientRequestModel)
admin.site.register(ClientModel)

