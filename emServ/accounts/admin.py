from django.contrib import admin

# Register your models here.

from accounts.models import UserProfile

admin.site.register(UserProfile)
