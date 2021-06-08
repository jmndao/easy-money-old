from django import forms
from dashboard.models import ProductModel



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'