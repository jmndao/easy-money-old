from django import forms
from django.forms import fields
from dashboard.models import (VenteModel, ProductModel, ClientModel, DevisModel)


class VenteForm(forms.ModelForm):

    class Meta:
        model = VenteModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(VenteForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0)
        else:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0, shop__owner__user=self.user)


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProductModelForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields['seller'].queryset = ClientModel.objects.filter(
                vente_or_achat='CV')
        else:
            self.fields['seller'].queryset = ClientModel.objects.filter(
                vente_or_achat='CV', shop__owner__user=self.user)


class DevisModelForm(forms.ModelForm):

    class Meta:
        model = DevisModel
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super(DevisModelForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields['client'].queryset = ClientModel.objects.filter(
                vente_or_achat='CR')
        else:
            self.fields['client'].queryset = ClientModel.objects.filter(
                vente_or_achat='CR', shop__owner__user=self.user)
