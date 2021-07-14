from django.urls import path
import clientRequests.views as cr_views

app_name = 'clientRequests'

urlpatterns = [
    # ClientRequest Routers
    path('', cr_views.ClientRequestView.as_view(), name="clientRequestPage"),
    path('modifier/<int:pk>/', cr_views.ClientRequestUpdateView.as_view(), name='clientRequestEditPage'),
    path('supprimer_plusieur/', cr_views.multiple_delete_clientRequest, name='multipleDeleteClientRequestPage'),
    path('detail/<int:pk>/', cr_views.ClientRequestDetailView.as_view(), name='clientRequestDetailPage'),
]
