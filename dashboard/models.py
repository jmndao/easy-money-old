from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
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
    ('CONNECTIQUE', 'Connectique'),
    ('LED', 'Led'),
    ('BIJOUX', 'Bijoux'),
    ('ENFANTS_ET_BÉBÉS', 'Enfants_et_bébés'),
    ('MONTRE', 'Montre'),
    ('ÉLECTROMÉNAGÉ', 'Électroménagé'),
    ('LIVRE', 'Livre'),
    ('FRIPERIE', 'Friperie'),
    ('JEUXVIDEO', 'Jeux Video'),
    ('LUXE', 'Luxe'),
    ('CUISINE', 'Cuisine'),
    ('AUTRES', 'Autre')     
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

    owner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, null=True, blank=True)
    emplacement = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)


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
    quantity = models.IntegerField(blank=False, null=False, default=1)
    initial_quantity = models.IntegerField(
        blank=True, null=True, default=1, editable=False)
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
    exact_dimension = models.IntegerField(null=True, blank=True, default=0)
    edition = models.CharField(max_length=100, null=True, blank=True)
    annee = models.CharField(max_length=20, null=True, blank=True)
    storage = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    charger = models.BooleanField(default=False)
    original_box = models.BooleanField(default=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(
        to='clients.ClientModel', null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    connectic = models.BooleanField(default=False)
    material = models.CharField(
        max_length=100, null=True, blank=True, default=None)
    garantie = models.BooleanField(default=False)
    delai_garantie = models.IntegerField(null=True, blank=True, default=True)

    def save(self, *args, **kwargs):
        import unidecode
        self.name = self.name.lower()
        self.name = unidecode.unidecode(self.name)
        if self.quantity == 1 or self.quantity == None:
            self.quantity = 1
        if self.initial_quantity == 1 or self.initial_quantity == None:
            self.initial_quantity = self.quantity
        self.price_total = self.price + self.montant_restauration
        if not self.price_total_tt_produit:
            self.price_total_tt_produit = self.price_total * self.quantity
        self.price_vente_minimum_ad = self.price_total * 2

        if self.dimension == 'MOYEN':
            self.price_vente_minimum_dv = float(self.price_total) * 1.35
        elif self.dimension == 'GRAND':
            self.price_vente_minimum_dv = float(self.price_total) * 1.38
        else:
            self.price_vente_minimum_dv = float(self.price_total) * 1.3

        return super(ProductModel, self).save(*args, **kwargs)

    def __str__(self):
        if self.dv_or_ad == 'DV':
            return '{} /{} /{} / {} cfa '.format(self.name, self.dv_or_ad, self.quantity, self.price_vente_minimum_dv)
        else:
            return '{} /{} /{} / {} cfa '.format(self.name, self.dv_or_ad, self.quantity, self.price_vente_minimum_ad)


@receiver(pre_delete, sender=UserProfile)
def set_admin_shop_owner(sender, instance, **kwargs):
    admin = UserProfile.objects.get(user__is_superuser=True)
    shop = Shop.objects.get(owner=instance)
    shop = admin
    shop.save()


class CompanyLogo(models.Model):
   logo = models.ImageField(upload_to="profiles/", default='default.png')