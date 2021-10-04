from django.db import models

# Create your models here.

PAYMENTMODE = [
    (1, 'Espèce'),
    (2, 'Chèque'),
    (3, 'Orange Money')
]

class Invoice(models.Model):

    """
        Model that will handles all invoices and generate proper data in
        pdf format. This is a many-to-one relationship connecting an invoice
        to multiple sale (VenteModel).
        Attributes:
            - client            : client (ClientModel [one-to-one])
            - payment_mode      : describe the way the customer has paid his items
            - vente             : foreign key to the item
            - created_date      : Date the invoice has been released
    """

    client = models.OneToOneField('clients.ClientModel', on_delete=models.CASCADE)
    payment_mode = models.IntegerField(choices=PAYMENTMODE, default=1)
    ventes = models.ManyToManyField('ventes.VenteModel')
    created_date = models.DateTimeField(auto_now_add=True)
    