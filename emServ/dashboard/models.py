from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages
from django.contrib import messages



MESSAGES_TAGS = {
    messages.INFO: 'info',
    50: 'critical',
}
# Create your models here.

QUALITE = [
    ('EXCELLENT', 'Excellente'),
    ('NORMAL', 'Normale'),
    ('MAUVAISE', 'Mauvaise')
]


class ProductModel(models.Model):
    """
        The model that hold all the information for a specific product.
        A product must include those listed information but not necessary all
        depending on the type of product it is.
        Therefore, this model will grow each time we judge necessary to add a
        new product characteristic to measure and hold in the database.
        We've got so far:
            - nom_du_produit        : name of the product
            - model                 : model of the product [electronic]
            - edition               : the edition of the product
            - annee                 : the year it has been bought by the client
            - nombre_de_giga        : number of giga [electronic: phone, computer...]
            - nombre_de_ram         : number of ram [electronic: mostly computer]
            - dimensions            : the dimensions [electronic: TV, computer, (phones), ...]
            - poids                 : the weight (masse) of the product
            - chargeur              : if it has a charger or not [ Yes or No ]
            - boite_origine         : It the client has brought its original box.
            - created_date          : the day and time all of these above information has been added.

    """
    nom_du_produit = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    annee = models.DateField()
    nombre_de_giga = models.IntegerField()
    nombre_de_ram = models.IntegerField()
    dimensions = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name="Dimensions")
    poids = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name="Masse")
    chargeurs = models.BooleanField(default=True)
    boite_origine = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)





    def __str__ (self):
        return '{}:{}'.format(self.nom_du_produit, self.annee)


# First Model --  Depot
class DepositStockModel(models.Model):
    """
        This model talks about all the products that the shops has bought.
        It keeps their records from the day the product has arrived in 
        the shop.
        It holds:
            - nom_du_vendeur    : the name of the saler
            - produit           : the product that has been sold
            - qualite           : quality of the product ('excellent','normall','bad')
            - date_d_achat      : date and time of the purchase
            - prix_d_achat      : the price the product has been purchased
    """
    nom_vendeur = models.CharField(max_length=100, blank=True, null=True)
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    qualite = models.CharField(max_length=20, choices=QUALITE)
    date_d_achat = models.DateTimeField(auto_now_add=True)
    prix_d_achat = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix d'achat")

    def __str__(self):
        return '{}:{}'.format(self.nom_vendeur, self.produit.nom_du_produit)


# Second Model -- Achat


class BuyingStockModel(models.Model):
    """
        The Buying Stock holds the information about the all transaction that the
        shop makes, i.e sales. Therefore, it keeps record of all sales in it.
        The data are:
            - produit           : the product in sale
            - date_de_vente     : the date and time the product is being sold
            - prix_de_vente     : the price of sale of the product
            - prix_de_vente_min : the minimum price of the product
            - prix_de_vente_fin : the final price the product has been sold
            - garantie          : the number of months the product is guaranteed to the client
    """

    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    date_de_vente = models.DateTimeField(auto_now_add=True)
    prix_de_vente_min = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name="Prix de vente minimum")
    prix_de_vente_fin = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name="Prix de vente final")
    garantie = models.BooleanField(default=False)
    delai_garantie = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{}'.format(self.produit.nom_du_produit, self.date_de_vente)


# Fourth Model -- Clients
class ClientModel(models.Model):
    """
        This is a model that hold client data so that we can keep
        track of all the client that has ever enter in the shop.
        Thus, we'll be able to link them with the newsletter and 
        if ever they have ask for a product that was not in the shop
        we'll have their personal data in here.
        This store:
            - prenom_client     : the first name of the client
            - nom_du_client     : the last name of the client
            - numero            : his phone numer if he wills to.
            - address_email     : his email address that will serve for newsletter
    """
    prenom_du_client = models.CharField(max_length=100)
    nom_du_client = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    address_email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Client/{}:{}'.format(self.prenom_du_client, self.nom_du_client)


# Third Model -- Client Request Model
class ClientRequestModel(models.Model):
    """
        The client request model will hold persistent data about a 
        request a client has made in the shop.
        Therefore each client has its own record of what he has ever order
        in the shop.
        The data we're keeping are:
            - prenom_du_client  : It's the first Name of the client
            - nom_du_client     : the last of the client
            ---------------------------: Those two above are held in ClientModel...
            - date_demander     : the date and time he has submitted this request
            - produit_demander  : the product he has requested 
            - produit_trouver   : if the shop has satisfied the client or no.
    """

    # prenom_du_client = models.CharField(max_length = 100)
    # nom_du_client = models.CharField(max_length = 100)
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    date_demander = models.DateTimeField(auto_now_add=True)
    produit_demander = models.CharField(max_length=100)
    produit_trouver = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Client/{}:{}:{}'.format(self.client.prenom_du_client, self.nom_du_client, self.produit_trouver)


class Shop(models.Model):
    """
        Shop has the products, the deposit, the sales, and all about the clients.
        Therefore, each shop has its own personal record of all of those 
        above models including the owner himself.
        It holds:
            - owner                 : owner of the shop
            - nom_de_la_boutique    : name of the shop
            - produits              : the products that it has 
            - depot                 : the deposit it has made
            - achat                 : the sales it has made
            - clients               : the client it has 
            - requete_client        : the client request
            - create_date.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nom_de_la_boutique = models.CharField(max_length=100)
    produits = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    depot = models.ForeignKey(DepositStockModel, on_delete=models.CASCADE)
    achat = models.ForeignKey(BuyingStockModel, on_delete=models.CASCADE)
    clients = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    requete_client = models.ForeignKey(ClientRequestModel, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str(self):

        return 'Shop/{}:{}'.format(self.nom_de_la_boutique, self.owner.username)

# class NotificationModel(models.Model):

#     NOTIFICATION_TYPES = [
#         (1, 'Message'),
#         (2, 'Deletion')
#     ]

#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_sender')
#     to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_to')
#     message = models.TextField()
#     notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
#     overview = models.CharField(max_length=90, blank=True, null=True)

#     def __str__(self):
#         return '[{}|{}]->{}'.format(self.sender, self.to, self.overview)