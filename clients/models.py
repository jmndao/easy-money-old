from django.db import models
from dashboard.models import Shop

# Create your models here.

CLIENT = [
    ('CR', 'Client Regulier'),
    ('CV', 'Vendeur')
]

SEXE = [
    (1, 'Homme'),
    (2, 'Femme')
]

class ClientModel(models.Model):
    """
        This is a model that hold client data so that we can keep
        track of all the client that has ever enter in the shop.
        Thus, we'll be able to link them with the newsletter and 
        if ever they have ask for a product that was not in the shop
        we'll have their personal data in here.
        This store:
            - shop              : shop in which the client has gone to
            - fname             : the first name of the client
            - lname             : the last name of the client
            - nationality       : nationality of the client
            - address           : address of the client
            - sexe              : the sexe of the client (Male or Female)
            - numero            : his phone numer if he wills to.
            - address_email     : his email address that will serve for newsletter
    """
    shop = models.ForeignKey(
        to='dashboard.Shop', on_delete=models.CASCADE, blank=True, null=True)
    fname = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name="First Name")
    lname = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name="Last Name")
    nationality = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE)
    age = models.IntegerField()
    numero = models.CharField(max_length=20, blank=True, null=True)
    id_card = models.IntegerField(blank =True, null=True)
    passport_number = models.IntegerField(blank =True, null = True)
    email = models.EmailField(blank=True, null=True)
    passage = models.IntegerField(default=0, blank=True, null=True)
    vente_or_achat = models.CharField(
        max_length=100, choices=CLIENT, default="CR")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['fname', 'lname', 'numero']

    def new_passage(self):
        self.passage += 1

    def __str__(self):
        return '{} {}'.format(self.fname, self.lname)
