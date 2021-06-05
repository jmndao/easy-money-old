from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

QUALITE = [
    ('EXCELLENT', 'Excellente'),
    ('NORMAL', 'Normale'),
    ('MAUVAISE', 'Mauvaise')
]


class ProductModel(models.Model):
    nom_du_produit = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    annee = models.DateTimeField()
    nombre_de_giga = models.IntegerField()
    nombre_de_ram = models.IntegerField()
    dimensions = models.DecimalField(max_digits = 8, decimal_places = 3, verbose_name = "dimensions")
    poids = models.DecimalField(max_digits = 8, decimal_places = 3, verbose_name = "dimensions")
    chargeurs = models.BooleanField(default = False)
    boite_origine = models.BooleanField(default = False)



# First Model --  Depot
class DepositStockModel(models.Model):
    nom_vendeur = models.CharField(max_length=100, blank=True, null=True)
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    qualite = models.CharField(max_length=20, choices=QUALITE)
    date_d_achat = models.DateTimeField(auto_now_add=True)
    prix_d_achat = models.DecimalField(max_digits = 8, decimal_places = 3, verbose_name = "prix d'achat" )


# Second Model -- Achat

class BuyingStockModel(models.Model):
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    date_de_vente = models.DateTimeField(default = datetime.now) 
    prix_de_vente_min = models.DecimalField(max_digits = 8, decimal_places=3, verbose_name="Prix de vente minimum")
    prix_de_vente_fin = models.DecimalField(max_digits = 8, decimal_places=3, verbose_name="Prix de vente final")
    garantie = models.BooleanField()
    delai_garantie = models.IntegerField()





# Third Model -- Demande Client
class demande_client(models.Model):
    prenom_du_client = models.CharField(max_length = 100)
    nom_du_client = models.CharField(max_length = 100)
    date_demander =  models.DateTimeField(auto_now_add=True)
    produit_demander = models.CharField(max_length = 100)
    produit_trouver = models.BooleanField(default = False)


# Fourth Model -- Clients
class ClientModel(models.Model):
    prenom_du_client = models.CharField(max_length = 100)
    nom_du_client = models.CharField(max_length = 100)
    numero = models.IntegerField(max_length=20)
    address_email = models.CharField(max_length = 100)


# Fifth Model -- Notifications

