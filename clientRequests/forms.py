from django import forms
from clientRequests.models import ClientRequestModel


class ClientRequestForm(forms.ModelForm):

    class Meta:
        model = ClientRequestModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientRequestForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs['class'] = 'select-with-search'
        self.fields['client'].empty_label = 'Clients'
        
