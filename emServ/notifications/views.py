from django.shortcuts import render
from django.views.generic import ListView, DetailView
from notifications.models import NotificationModel
from message.models import Message

# Create your views here.


class NotificationView(ListView):

    model = NotificationModel
    template_name = 'notifications/notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(to=self.request.user)
        return context
    


class NotificationDetailView(DetailView):

    model = NotificationModel
    template_name = 'notifications/notification_detail.html'
