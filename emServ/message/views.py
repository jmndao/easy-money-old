from django.contrib.auth import models
from django.shortcuts import render
from django.urls import reverse_lazy
from notifications.signals import notify
from message.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

# Create your views here.


class MessageView(LoginRequiredMixin, CreateView):

    template_name = 'message/message.html'
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('message:messagePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["msgs"] = Message.objects.all().order_by('-created_date')
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        notify.send(
            form.instance.sender,
            recipient=form.instance.to,
            description=form.instance.text_message,
            verb=form.instance.subject
        )
        return super().form_valid(form)
    

        
    


