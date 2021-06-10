from django.urls import path
import message.views as m_views


app_name = 'message'

urlpatterns = [
    path('', m_views.MessageView.as_view(), name='messagePage'),
]
