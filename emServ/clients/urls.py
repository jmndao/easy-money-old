from django.urls import path
import clients.views as c_views


app_name = 'clients'

urlpatterns = [
    # Client Routers
    path('', c_views.ClientView.as_view(), name="clientPage"),
    path('modifier/<int:pk>/', c_views.ClientUpdateView.as_view(), name='clientEditPage'),
    path('supprimer/<int:pk>/', c_views.ClientDeleteView.as_view(), name='clientDeletePage'),
    path('supprimer_plusieur/', c_views.multiple_delete_client, name='multipleDeleteClientPage'),
    path('detail/<int:pk>/', c_views.ClientDetailView.as_view(), name='clientDetailPage'),
]
