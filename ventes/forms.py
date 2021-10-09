from django import forms
from django.forms import fields
from django.forms.models import inlineformset_factory
from dashboard.models import ProductModel
from ventes.models import VenteModel


class VenteForm(forms.ModelForm):

    class Meta:
        model = VenteModel
        fields = ['produit', 'price', 'acompte', 'quantity', 'guarantee', 'guarantee_period']
    
    class Meta:
        model = VenteModel
        fields = ['price']
        error_messages = {
            'price': {
                'required': "This is a custom error message from modelform meta",
            },
        }

    def __init__(self, *args, **kwargs):
        super(VenteForm, self).__init__(*args, **kwargs)
        self.fields['produit'].widget.attrs['class'] = 'select-with-search'
        self.fields['produit'].empty_label = 'Produits'
        self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0)
        # if self.user.is_superuser:
        #     self.fields['produit'].queryset = ProductModel.objects.filter(
        #         quantity__gt=0)
        # else:
        #     self.fields['produit'].queryset = ProductModel.objects.filter(
        #         quantity__gt=0, shop__owner__user=self.user)
