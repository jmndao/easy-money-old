from import_export import resources
from import_export.fields import Field
from dashboard.models import ProductModel
from ventes.models import VenteModel
from clients.models import ClientModel

class ProductExcel(resources.ModelResource):
    shop__name = Field(attribute='shop__name', column_name='Boutique')
    name = Field(attribute='published', column_name='Nom Produit')
    price = Field(attribute='price', column_name='Prix')
    category = Field(attribute='category', column_name='Categorie')
    quantity = Field(attribute='quantity', column_name='Quantite')
    montant_restauration = Field(attribute='montant_restauration', column_name='Montant Restauration')
    dv_or_ad = Field(attribute='dv_or_ad', column_name='Depot ou Achat')
    shop__owner__user__username = Field(attribute='shop__owner__user__username', column_name='Agent Responsable')
    created_date = Field(attribute='created_date', column_name="Date d'Ajout")

    class Meta:
        model = ProductModel
        fields = ['shop__name', 'name', 'price', 'catgory', 'quantity', 'montant_restauration', 'dv_or_ad', 'shop__owner__user__username', 'created_date']


class VenteExcel(resources.ModelResource):

    class Meta:
        model = VenteModel
        fields = ['produit__name', 'price', 'price_total', 'acompte', 'restant_du', 'quantity', 'client__fname', 'client__lname', 'quantity', 'created_date']


class ClientExcel(resources.ModelResource):

    class Meta:
        model = ClientModel
        fields =['shop__owner__user__username', 'fname', 'lname', 'sexe', 'numero', 'created_date']