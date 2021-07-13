from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from dashboard.models import ProductModel
from clients.models import ClientModel

# Create your models here.


class NotificationModel(models.Model):

    NOTIFICATION_TYPES = [
        (1, 'Message'),
        (2, 'Suppression'),
        (3, 'Ajout'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_sender')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_to')
    message = models.TextField()
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=ProductModel)
    def create_notif_product_post(sender, created, instance, **kwargs):
        if created:
            if not instance.shop.owner.user.is_superuser:
                users = User.objects.filter(is_superuser=True)
                for user in users:
                    msg = "Produit {} vient d'être ajouté par {}".format(instance.name, instance.shop.owner.user)
                    NotificationModel.objects.create(
                        sender = instance.shop.owner.user,
                        to = user,
                        message = msg,
                        notification_type = 2).save()

    @receiver(post_delete, sender=ProductModel)
    def create_notif_product_delete(sender, instance, *args, **kwargs):
        if not instance.shop.owner.user.is_superuser:
            users = User.objects.filter(is_superuser=True)
            for user in users:
                msg ="Produit {} vient d'être supprimé par {}".format(instance.name, instance.shop.owner.user)
                NotificationModel.objects.create(
                    sender=instance.shop.owner.user,
                    to=user,
                    message=msg,
                    notification_type=1).save()

    def __str__(self):
        return '{} {}'.format(self.notification_type, self.sender)