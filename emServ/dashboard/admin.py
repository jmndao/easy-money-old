from django.contrib import admin

# Register your models here.
from dashboard.models import ProductModel, Shop 

admin.site.register(ProductModel)
admin.site.register(Shop)

