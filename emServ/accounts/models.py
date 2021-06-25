from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

GENDER = [
    (1, 'Male'),
    (2, 'Femelle')
]


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop_user_related")
    avatar = models.ImageField(upload_to="profiles/", default='default.png')
    phone_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numero de Telephone")
    agency = models.CharField(max_length=100, blank=True, null=True, verbose_name="Agence")
    gender = models.IntegerField(choices=GENDER, blank=True, null=True, default=1)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_default_userprofile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_default_userprofile(sender, instance, **kwargs):
        instance.shop_user_related.save()

    def __str__(self):
        return '{}'.format(self.user.username)


