from django import forms
from dashboard.models import ProductModel,ClientModel,DepotVenteStockModel



class ProductModelForm(forms.Form):
    class Meta:
        model = ProductModel
        fields = '__all__'

class DepotVenteModel(forms.Form):
    class Meta:
        model = DepotVenteStockModel
        fields = [
            'nom_vendeur',
            'produit',
            'quantite',
            'prix_d_depot'
        ]