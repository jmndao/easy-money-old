from django.db import models
from dashboard.models import Shop, ClientModel

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
    reparatinon_price = models.IntegerField(null=True, blank=True, default=0)
    category = models.CharField(
        max_length=100, choices=CATEGORY, blank=True, null=True)
    final_price = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        self.used_price = self.new_price / 2
        return super(EstimationModel, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.product_name)
