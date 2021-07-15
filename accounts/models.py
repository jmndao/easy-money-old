from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

# Create your models here.

GENDER = [
    ("H", 'Homme'),
    ("F", 'Femme')
]


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, related_name="shop_user_related")
    avatar = models.ImageField(upload_to="profiles/", default='default.png')
    cin = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Numero de Telephone")
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.user.username)

    
@receiver(post_save, sender=User)
def create_default_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_default_userprofile(sender, instance, **kwargs):
    instance.shop_user_related.save()


@receiver(post_delete, sender=User)
def delete_shop(sender, instance, **kwargs):
    instance.shop_user_related.delete()
