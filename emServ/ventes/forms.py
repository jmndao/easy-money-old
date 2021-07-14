from django import forms
from dashboard.models import ProductModel
from ventes.models import VenteModel


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