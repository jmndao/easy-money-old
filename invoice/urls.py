from django.urls import path
import invoice.views as i_views

app_name = 'invoice'

urlpatterns = [
    path("", i_views.InvoiceView.as_view(), name='invoicePage'),
]
