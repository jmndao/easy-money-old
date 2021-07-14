"""easy_money URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('client_request/', include('clientRequests.urls')),
    path('clients/', include('clients.urls')),
    path('ventes/', include('ventes.urls')),
    path('estimation/', include('estimation.urls')),
    path('devis/', include('devis.urls')),
    path('search/', include('search.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'dashboard.views.error_404'
# handler404 = 'estimation.views.error_404'

handler500 = 'dashboard.views.error_500'
# handler500 = 'estimation.views.error_500'


