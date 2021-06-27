from django import forms
from django.forms import fields
from message.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
