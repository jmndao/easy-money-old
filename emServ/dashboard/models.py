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
    ('DECORATIONS', 'Decorations'),
    ('ENFANT', 'Telephoniques'),
    ('AMMEUBLEMENT', 'Ammeublement'),
    ('LOISIRS', 'Loisirs'),
    ('IMAGES_ET_SONS', 'Images_et_sons'),
    ('AUTRES', 'Autre'),
]

ETAT = [
    ('NEUF', 'Neuf'),
    ('BON', 'Bon'),
    ('MOYEN', 'Moyen'),
    ('MAUVAIS', 'Mauvais'),
    ('POUR_PIECE', 'Pour Piece')
]

TYPE = [
    ('DV', 'Depot Vente'),
    ('AD', 'Achat Direct')
]

OBSOLESCENCE = [
    ('TRES_RAPIDE', 'Tres_Rapide'),
    ('RAPIDE', 'Rapide'),
    ('MOYENNE', 'Moyenne'),
    ('LENTE', 'Lente')
]

RARETE = [
    ('RARE', 'Rare'),
    ('COURANT', 'Courant'),
    ('TRES_COURANT', 'Tres courant')
]

CHARGEUR = [
    ('OUI', 'Oui'),
    ('NON', 'Non'),
    ('PAS_BESOIN', 'Pas_besoin'),
]

DIMENSION = [
    ('PETIT', 'Petit'),
    ('MOYEN', 'Moyen'),
    ('GRAND', 'Grand')
]

ACHATVENTE = [
    ('ACHAT', 'Achat'),
    ('VENTE', 'Vente')
]

CLIENT = [
    ('CR', 'Client Regulier'),
    ('CV', 'Vendeur')
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

        return '{} {}'.format(self.name, self.owner.user.username)


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
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    fname = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name="First Name")
    lname = models.CharField(max_length=100, blank=True,
                             null=True, verbose_name="Last Name")
    nationality = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE)
    age = models.IntegerField()
    numero = models.CharField(max_length=20, blank=True, null=True)
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
            - dv_or_ad              : category depot vente or achat direct
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
            -montatnt_restauration  : The amount spent to fix the product.
            -description            : To give a quick description of the product we're putting in.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    model = models.CharField(max_length=100,  null=True, blank=True)
    category = models.CharField(
        max_length=100, choices=CATEGORY, blank=True, null=True)
    dv_or_ad = models.CharField(
        max_length=100, choices=TYPE, blank=True, null=True)
    quantity = models.IntegerField(blank=False, null=False,default = 1)
    initial_quantity = models.IntegerField(blank=True, null=True,default = 1, editable=False)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Prix d'Achat")
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix D'Achat Total", blank=True, null=True)
    montant_restauration = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Montant de la Restauration")
    estate = models.CharField(
        max_length=20, choices=ETAT, blank=True, null=True)
    obsolescence = models.CharField(
        max_length=20, choices=OBSOLESCENCE, blank=True, null=True)
    rarety = models.CharField(
        max_length=20, choices=RARETE, blank=True, null=True)
    sale_bill = models.BooleanField(default=False)
    dimension = models.CharField(
        max_length=20, choices=DIMENSION, null=True, blank=True)
    edition = models.CharField(max_length=100, null=True, blank=True)
    annee = models.CharField(max_length=20, null=True, blank=True)
    storage = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    charger = models.BooleanField(default=False)
    original_box = models.BooleanField(default=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(
        ClientModel, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    color = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.price_total = self.price * self.quantity
        if self.initial_quantity == 1 or self.initial_quantity == None:
            self.initial_quantity = self.quantity
        return super(ProductModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{} /{} /{} / {} '.format(self.name, self.dv_or_ad, self.quantity, self.price)


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
    """

    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix d'achat")
    client = models.ForeignKey(
        ClientModel, on_delete=models.SET_NULL, null=True, blank=True)
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
            - price             : price the product has been given to the shop

        Notice that the diffrence is going to be in which page, the user went to fill the form
    """
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.DecimalField(
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
            - acompte           : the amount of money that the client has given at this moment
    """

    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente Final", blank=True, null=True)
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente Final", blank=True, null=True)
    acompte = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="L'avance du client", blank=True, null=True)
    guarantee = models.BooleanField(default=False)
    client = models.ForeignKey(
        ClientModel, on_delete=models.SET_NULL, blank=True, null=True)
    guarantee_period = models.IntegerField(
        blank=True, null=True, verbose_name="Periode de garantie [en mois]")
    created_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True, default=1)

    def save(self, *args, **kwargs):
        self.price_total = self.price * self.quantity
        return super(VenteModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.produit.name, self.price)


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
        return '{} {} {}'.format(self.client.fname, self.client.lname, self.found)


# Model -- Devis Model
class DevisModel(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    quantity = models.IntegerField(blank=False, null=False, default=1)
    price = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="prix proposed")
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="prix proposed")
    client = models.ForeignKey(
        ClientModel, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        self.price_total = self.price * self.quantity
        return super(DevisModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {} {}'.format(self.client.fname, self.client.lname, self.product_name)

# Estimation Model


class EstimationModel(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    seller = models.ForeignKey(
        ClientModel, null=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=100)
    new_price = models.DecimalField(
        max_digits=20, decimal_places=3, blank=False, null=True, verbose_name="Prix neuf")
    used_price = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Prix occasion")
    estate = models.CharField(
        max_length=20, choices=ETAT, blank=False, null=True)
    obsolescence = models.CharField(
        max_length=20, choices=OBSOLESCENCE, blank=False, null=True)
    rarety = models.CharField(
        max_length=20, choices=RARETE, blank=False, null=True)
    sale_bill = models.BooleanField(default=False)
    dimension = models.CharField(
        max_length=20, choices=DIMENSION, null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    charger = models.CharField(
        max_length=20, choices=CHARGEUR, null=True, blank=False)
    original_box = models.BooleanField(default=False)
    year_of_release = models.IntegerField(null=True, blank=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    reparatinon_price = models.IntegerField(null=True, blank=True, default= 0)
    category = models.CharField(
        max_length=100, choices=CATEGORY, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        self.used_price = self.new_price / 2
        return super(EstimationModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.product_name)
