from django import forms
from dashboard.models import ProductModel
from ventes.models import VenteModel


class VenteForm(forms.ModelForm):

    class Meta:
        model = VenteModel
        fields = '__all__'
    

    # class Meta:
    #     model = VenteModel
    #     fields = ['price']
    #     error_messages = {
    #         'price': {
    #             'required': "This is a custom error message from modelform meta",
    #         },
    #     }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(VenteForm, self).__init__(*args, **kwargs)
        self.fields['produit'].widget.attrs['class'] = 'select-with-search'
        self.fields['client'].widget.attrs['class'] = 'select-with-search'
        self.fields['produit'].empty_label = 'Produits'
        self.fields['client'].empty_label = 'Clients'
        if self.user.is_superuser:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0)
        else:
            self.fields['produit'].queryset = ProductModel.objects.filter(
                quantity__gt=0, shop__owner__user=self.user)

   