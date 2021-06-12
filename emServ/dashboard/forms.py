from django import forms
from dashboard.models import ProductModel,ClientModel



class ProductModelForm(forms.Form):
    class Meta:
        model = ProductModel
        fields = '__all__'