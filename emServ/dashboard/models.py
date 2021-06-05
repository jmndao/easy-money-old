from django.db import models
from django.urls import reverse

# Create your models here.

QUALITE = [
    ('EXCELLENT', 'Excellente'),
    ('NORMAL', 'Normale'),
    ('MAUVAISE', 'Mauvaise')
]

class ProductModel(models.Model):

    nom = models.CharField(max_length=100)
    commentaire = models.TextField()

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


# Fourth Model -- Clients


# Fifth Model -- Notifications
