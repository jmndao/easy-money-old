from django import forms
from dashboard.models import ProductModel,ClientModel



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'

class ClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = '__all__'