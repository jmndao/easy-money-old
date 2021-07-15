from django.db import models

# Create your models here.

# Model -- Vente
class VenteModel(models.Model):
    """
        The Sale Stock holds the information about the all transaction that the
        shop makes, i.e sales. Therefore, it keeps record of all sales in it.
        The data are:

            - produit           : the product in sale
            - created_date      : the date and time the product is being sold
            - price             : the final price the product has been sold
            - garantee          : the number of months the product is guaranteed to the client
            - guarantee_period  : the period in which the guarantee is valid in months
            - acompte           : the amount of money that the client has given at this moment
    """

    produit = models.ForeignKey(to='dashboard.ProductModel', on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente", blank=True, null=True)
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente Final", blank=True, null=True)
    acompte = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="L'avance du client", blank=True, null=True, default = 0)
    restant_du = models.DecimalField( decimal_places=3, verbose_name="Restant du Client", blank=True, null=True, max_digits=20, default = 0)
    guarantee = models.BooleanField(default=False)
    client = models.ForeignKey(
        to='clients.ClientModel', on_delete=models.SET_NULL, blank=True, null=True)
    guarantee_period = models.IntegerField(
        blank=True, null=True, verbose_name="Periode de garantie [en mois]")
    created_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True, default=1)

    def save(self, *args, **kwargs):
        self.price_total = self.price * self.quantity
        if self.acompte != 0 or None: 
            self.restant_du = self.price_total -  self.acompte
        else: 
            self.restant_du = 0
        return super(VenteModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.produit.name, self.price)
