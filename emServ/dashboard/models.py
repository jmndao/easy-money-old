from django.db import models
from django.urls import reverse

# Create your models here.

QUALITE = [
    ('EXCELLENT', 'Excellente'),
    ('NORMAL', 'Normale'),
    ('MAUVAISE', 'Mauvaise')
]


class ProductModel(models.Model):
    nom_du_produit = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    Edition = models.CharField(max_length=100)
    annee = models.DateTimeField()
    nombre_de_gigo = models.IntegerFileld(max_digits = 4)
    nombre_de_ram = models.IntegerField(max_digits = 2)
    dimensions = models.DecimalField()
    poids = models.DecimalField()
    chargeurs = models.BooleanField(default = 'False')
    boite_origine = models.BooleanField(default = 'False')



# First Model --  Depot
class DepositStockModel(models.Model):

    nom_vendeur = models.CharField(max_length=100, blank=True, null=True)
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    qualite = models.CharField(max_length=20, choices=QUALITE)
    date_d_achat = models.DateTimeField(auto_now_add=True)
    prix_d_achat = models.DecimalField(max_digits=20, decimal_places=3)


# Second Model -- Achat

class BuyingStockModel(models.Model):

    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    date_de_vente = models.DateTimeField()
    prix_de_vente_min = models.DecimalField(max_digits=20, decimal_places=3, verbose_name="Prix de vente minimum")
    prix_de_vente_fin = models.DecimalField(max_digits=20, decimal_places=3, verbose_name="Prix de vente final")
    garantie = models.BooleanField()





# Third Model -- Demande Client
class demande_client(models.Model):
    prenom_du_client = models.CharacterFields(max_length = 100)
    nom_du_client = models.CharacterFields(max_length = 100)
    date_demander =  models.DateTimeField(auto_now_add=True)
    produit_demander = models.CharacterFields(max_length = 100)
    produit_trouver = models.BooleanField(default = 'False')


# Fourth Model -- Clients
class ClientModel(models.Model):
    prenom_du_client = models.CharacterFields(max_length = 100)
    nom_du_client = models.CharacterFields(max_length = 100)
    numero = models.IntegerFields(max_length=20)
    address_email = models.CharacterFields(max_length = 100)


# Fifth Model -- Notifications

