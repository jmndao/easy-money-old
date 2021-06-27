from django.shortcuts import render
from django.views.generic import ListView, DetailView
from notifications.models import NotificationModel
from message.models import Message
from notifications.forms import MessageForm
from dashboard.utils import Utils

# Create your views here.


class NotificationView(ListView, Utils):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_notif_as_read(NotificationModel)

    template_name = 'notifications/notification.html'
    context_object_name = 'notifications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(to=self.request.user)
        context['message_form'] = MessageForm()
        return context

    def get_queryset(self):
        return NotificationModel.objects.filter(to=self.request.user)
    
    


class NotificationDetailView(DetailView):

    model = NotificationModel
    template_name = 'notifications/notification_detail.html'
