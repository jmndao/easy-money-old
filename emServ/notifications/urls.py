from django.urls import path
import notifications.views as n_views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', n_views.NotificationView.as_view(), name='notificationPage'),
]
