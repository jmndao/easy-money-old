from django.views.generic import ListView, DetailView
from notifications.models import NotificationModel
from dashboard.utils import Utils

# Create your views here.


class NotificationView(ListView, Utils):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_notif_as_read(NotificationModel)

    template_name = 'notifications/notification.html'
    model = NotificationModel
    context_object_name = 'notifications'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notification"
        return context

    def get_queryset(self):
        return NotificationModel.objects.filter(to=self.request.user)
    
    


class NotificationDetailView(DetailView):

    model = NotificationModel
    template_name = 'notifications/notification_detail.html'
