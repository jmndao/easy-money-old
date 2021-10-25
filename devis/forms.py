from django import forms
from devis.models import DevisModel
from clients.models import ClientModel
from dashboard.models import ProductModel


class DevisModelForm(forms.ModelForm):

    class Meta:
        model = DevisModel
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')
        super(DevisModelForm, self).__init__(*args, **kwargs)
        self.fields['produit'].widget.attrs['class'] = 'select-with-search'
        self.fields['client'].widget.attrs['class'] = 'select-with-search'
        self.fields['produit'].empty_label = 'Produits'
        self.fields['client'].empty_label = 'Clients'
        if self.user.is_superuser:
            self.fields['client'].queryset = ClientModel.objects.filter(
                vente_or_achat='CR')
        else:
            self.fields['client'].queryset = ClientModel.objects.filter(
                vente_or_achat='CR', shop__owner__user=self.user)
            self.fields['produit'].queryset = ProductModel.objects.filter(
                shop__owner__user=self.user)