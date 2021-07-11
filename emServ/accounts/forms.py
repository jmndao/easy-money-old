from django import forms
from accounts.models import UserProfile


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=225)
    last_name = forms.CharField(max_length=225)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):

    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg