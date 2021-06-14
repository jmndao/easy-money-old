from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.db.models.signals import post_save

# Create your models here.

GENDER = [
    (1, 'Male'),
    (2, 'Femelle')
]


class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shop_user_related")
    avatar = models.ImageField(upload_to="profiles/avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numero de Telephone")
    agency = models.CharField(max_length=100, blank=True, null=True, verbose_name="Agence")
    gender = models.IntegerField(choices=GENDER, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return 'User/{}:{}'.format(self.user.username, self.full_name)

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')


def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)