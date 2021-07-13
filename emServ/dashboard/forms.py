from django import forms
from dashboard.models import ProductModel
from clients.models import ClientModel


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

