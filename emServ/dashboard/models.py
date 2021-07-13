from django.db import models
from django.urls import reverse
from clients.models import ClientModel
from accounts.models import UserProfile


# Create your models here.

SEXE = [
    ('H', 'Homme'),
    ('F', 'Femme')
]

CATEGORY = [
    ('TELEPHONE', 'Telephone'),
    ('TABLETTE', 'Tablette'),
    ('ORDINATEUR', 'Ordinateur'),
    ('TELEVISION', 'Television'),
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
    price_total_tt_produit = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix D'Achat Total", blank=True, null=True)
    price_vente_minimum_ad = models.DecimalField(
        max_digits=20, decimal_places=0, verbose_name="Prix Vente Minimu", blank=True, null=True, editable=True)
    price_vente_minimum_dv = models.DecimalField(
        max_digits=20, decimal_places=0, verbose_name="Prix Vente Minimu", blank=True, null=True, editable=True)
    montant_restauration = models.DecimalField(
        max_digits=20, decimal_places=3, blank=True, null=True, verbose_name="Montant de la Restauration", default=0)
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
    connectic = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if self.quantity == 1 or self.quantity == None:
            self.quantity = 1
        if self.initial_quantity == 1 or self.initial_quantity == None:
            self.initial_quantity = self.quantity
        self.price_total = self.price + self.montant_restauration
        if not self.price_total_tt_produit:
            self.price_total_tt_produit = self.price_total * self.quantity
        self.price_vente_minimum_ad = self.price_total * 2
        self.price_vente_minimum_dv = float(self.price_total) * 1.3
        return super(ProductModel, self).save(*args, **kwargs)

    def __str__(self):
        if self.dv_or_ad == 'DV':
            return '{} /{} /{} / {}cfa '.format(self.name, self.dv_or_ad, self.quantity, self.price_vente_minimum_dv)
        else:
            return '{} /{} /{} / {}cfa '.format(self.name, self.dv_or_ad, self.quantity, self.price_vente_minimum_ad)


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
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente", blank=True, null=True)
    price_total = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="Prix De Vente Final", blank=True, null=True)
    acompte = models.DecimalField(
        max_digits=20, decimal_places=3, verbose_name="L'avance du client", blank=True, null=True, default = 0)
    restant_du = models.DecimalField( decimal_places=3, verbose_name="Restant du Client", blank=True, null=True, max_digits=20, default = 0)
    guarantee = models.BooleanField(default=False)
    client = models.ForeignKey(
        ClientModel, on_delete=models.SET_NULL, blank=True, null=True)
    guarantee_period = models.IntegerField(
        blank=True, null=True, verbose_name="Periode de garantie [en mois]")
    created_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True, default=1)

    def save(self, *args, **kwargs):
        # self.price_total = self.price * self.quantity
        if self.acompte != 0 or None: 
            self.restant_du = self.price_total -  self.acompte
        else: 
            self.restant_du = 0
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
    wished_price = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return '{} {} {}'.format(self.client.fname, self.client.lname, self.found)


# Model -- Devis Model
class DevisModel(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, blank=True, null=True)
    produit = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
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
    new_price = models.IntegerField(
        blank=False, null=True, verbose_name="Prix neuf")
    used_price = models.IntegerField(
        blank=True, null=True, verbose_name="Prix occasion")
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
    final_price = models.IntegerField(null=True, blank=True, default= 0)
    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        self.used_price = self.new_price / 2
        return super(EstimationModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.product_name)
