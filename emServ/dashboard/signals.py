from django.dispatch import receiver
from django.db.models.signals import post_save
from dashboard.models import ClientModel


@receiver(post_save, sender=ClientModel)
def increment_passage(sender, created, instance, **kwargs):
    if created:
        client = ClientModel.objects.get(pk=instance.pk)
        client.passage += 1
        client.save()
        

