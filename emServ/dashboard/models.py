from django.db import models
from django.urls import reverse
from accounts.models import UserProfile


# Create your models here.

SEXE = [
    ('H', 'Homme'),
    ('F', 'Femme')
]

CATEGORY = [
    ('ELECTRONIQUE', 'Electronique'),
    ('VETEMENT', 'Vetement'),
    ('AUTRES', 'Autre')
]

ETAT = [
    ('NEUF', 'Neuf'),
    ('BON', 'Bon'),
    ('MOYEN', 'Moyen'),
    ('MAUVAIS', 'Mauvais'),
    ('POUR_PIECE', 'Pour Piece')
]

OBSOLESCENCE = [
    ('RAPIDE', 'Rapide'),
    ('MOYENNE', 'Moyenne'),
    ('LENTE', 'Lente')
]

RARETE = [
    ('RARE', 'Rare'),
    ('COURANT', 'Courant'),
    ('TRES_COURANT', 'Tres courant')
]

DIMENSION = [ 
    ('PETIT', 'Petit'),
    ('MOYEN', 'Moyen'),
    ('GRAND', 'Grand')
]


class Shop(models.Model):
    """
        Shop has the products, the deposit, the sales, and all about the clients.
        Therefore, each shop has its own personal record of all of those 
        above models including the owner himself.
        It holds:
            - owner                 : owner of the shop
            - name                  : name of the shop
            - emplacement           : where the shop is situated
            - create_date.
    """

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    emplacement = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return 'Shop/{}:{}'.format(self.name, self.owner.user.username)


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
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100, blank=True, null=True, verbose_name="First Name")
    lname = models.CharField(max_length=100, blank=True, null=True, verbose_name="Last Name")
    nationality = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE)
    age = models.IntegerField()
    numero = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Client/{}:{}'.format(self.fname, self.lname)



class ProductModel(models.Model):
    """
        The model that hold all the information for a specific product.
        A product must include those listed information but not necessary all
        depending on the type of product it is.
        Therefore, this model will grow each time we judge necessary to add a
        new product characteristic to measure and hold in the database.
        We've got so far:
            - name                  : name of the product
            - model                 : model of the product [electronic]
            - category              : category of the product wheter its elec or ...
            - sale_price_on_new     : price of a such a new product
            - sale_price_on_old     : price of a such an old product
            - estate                : the actual estate of the product
            - obsolescence          : the rate of degradation of the product
            - rarety                : rarety or scarcety of the product
            - sale_bill             : the bill which state the sale of the product
            - edition               : the edition of the product
            - annee                 : the year it has been bought by the client
            - storage               : number of giga [electronic: phone, computer...]
            - ram                   : number of ram [electronic: mostly computer]
            - dimensions            : the dimensions [electronic: TV, computer, (phones), ...]
            - charger               : if it has a charger or not [ Yes or No ]
            - original_box          : It the client has brought its original box.
            - price                 : If it's Depot Vente (see line: 192) - that price so
            - description           : description of the product
            - created_date          : the day and time all of these above information has been added.

    """
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100,  null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY)
    quantity = models.IntegerField()
    sale_price_on_new = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Prix de Vente Neuf")
    sale_price_on_old = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Prix de Vente Occasion")
    estate = models.CharField(max_length=20, choices=ETAT)
    obsolescence = models.CharField(max_length=20, choices=OBSOLESCENCE)
    rarety = models.CharField(max_length=20, choices=RARETE)
    sale_bill = models.BooleanField(default=False)
    dimension = models.CharField(max_length=20, choices=DIMENSION)
    edition = models.CharField(max_length=100, null=True, blank=True)
    annee = models.CharField(max_length=20, null=True, blank=True)
    storage = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    charger = models.BooleanField(default=True)
    original_box = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Prix Depot Vente")
    seller = models.OneToOneField(ClientModel)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__ (self):
        return '{}[{}]'.format(self.name, self.category)



# Model --  Achat Direct 
class AchatDirectModel(models.Model):
    """
        This model talks about all the products that the shops has bought directly
        from the owner (client).
        It keeps their records from the day the product has arrived in 
        the shop.
        It holds:
            - produit           : the product that has been sold
            - created_date      : date and time of the sale
            - price             : the price the product has been purchased
            - min_price         : Minimal price the product has to be sold
    """
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix d'achat")
    min_price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix de vente minimum", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}[{}]'.format(self.produit.seller, self.produit.name)



# Depot Vente Model
class DepotVenteModel(models.Model):
    """
        This model represents the model in which, clients depose their belongings
        hoping that the company is going to sell it for them. And the company will 
        take its part after selling it. It basically has everything that the depositModel has.
        It holds:

            - produit           : the product that has been sold
            - created_date      : date and time of the purchase

        Notice that the diffrence is going to be in which page, the user went to fill the form
    """
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    min_price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix de vente minimum", blank=True, null=True)    
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}[{}]'.format(self.produit.name, self.produit.name)



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
    """

    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente Final", blank=True, null=True)
    guarantee = models.BooleanField(default=False)
    guarantee_period = models.IntegerField(blank=True, null=True, verbose_name="Periode de garantie [en mois]")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{}'.format(self.produit.name, self.price)



# Model -- Client Request Model
class ClientRequestModel(models.Model):
    """
        The client request model will hold persistent data about a 
        request a client has made in the shop.
        Therefore each client has its own record of what he has ever order
        in the shop.
        The data we're keeping are:

            - nom_du_client     : the last of the client
            ---------------------------: Those two above are held in ClientModel...
            - produit_demander  : the product he has requested 
            - found             : if the shop has satisfied the client or no.
    """

    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    produit_demander = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    found = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Client/{}:{}:{}'.format(self.client.prenom_du_client, self.nom_du_client, self.produit_trouver)


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