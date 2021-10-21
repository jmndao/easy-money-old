from django import forms
from django.forms import fields
from django.forms.models import inlineformset_factory
from dashboard.models import ProductModel
from ventes.models import VenteModel


class VenteForm(forms.ModelForm):

    class Meta:
        model = VenteModel
        fields = ['produit', 'price', 'acompte',
                  'quantity', 'guarantee', 'guarantee_period']

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
        self.fields['type_de_service'].widget.attrs['class'] = 'select-with-search'
        self.fields['produit'].empty_label = 'Produits'
        self.fields['produit'].queryset = ProductModel.objects.filter(
            quantity__gt=0)
        # if self.user.is_superuser:
        #     self.fields['produit'].queryset = ProductModel.objects.filter(
        #         quantity__gt=0)
        # else:
        #     self.fields['produit'].queryset = ProductModel.objects.filter(
        #         quantity__gt=0, shop__owner__user=self.user)


class VenteFormSingle(forms.ModelForm):

    class Meta:
        model = VenteModel
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(VenteFormSingle, self).__init__(*args, **kwargs)
        self.fields['produit'].widget.attrs['class'] = 'select-with-search'
        self.fields['client'].widget.attrs['class'] = 'select-with-search'
        self.fields['produit'].empty_label = 'Produits'
        self.fields['client'].empty_label = 'Clients'
        self.fields['type_de_service'].widget.attrs['class'] = 'select-with-search'
        self.fields['type_de_service'].empty_label = 'Type de Service'
        self.fields['type_de_reglement'].widget.attrs['class'] = 'textarea_cls'
        if self.user.is_superuser:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0)
        else:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0, shop__owner__user=self.user)
