from django.db import models

# Create your models here.

# Model -- Devis Model
class DevisModel(models.Model):
    shop = models.ForeignKey(
        to='dashboard.Shop', on_delete=models.CASCADE, blank=True, null=True)
    produit = models.ForeignKey(to='dashboard.ProductModel', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False, default=1)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="prix proposed")
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="prix proposed")
    price_remise = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True)
    client = models.ForeignKey(
        to='clients.ClientModel', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.price_total = self.price * self.quantity
        return super(DevisModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {} {}'.format(self.client.fname, self.client.lname, self.product_name)
