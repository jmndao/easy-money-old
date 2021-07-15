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
    produit__shop__name = Field(attribute='produit__shop__name', column_name='Boutique')
    produit__name = Field(attribute='produit__name', column_name='Produit')
    price = Field(attribute='price', column_name='Prix de Vente')
    quantity = Field(attribute='quantity', column_name='Quantite')
    price_total = Field(attribute='price_total', column_name='Prix Total')
    client__fname = Field(attribute='client__fname', column_name='Prenom client')
    client__lname = Field(attribute='client__lname', column_name='Nom client')
    client__numero = Field(attribute='client__numero', column_name='Numero Telephone')
    client__email = Field(attribute='client__email', column_name='Email')
    acompte = Field(attribute='acompte', column_name='Acompte')
    created_date = Field(attribute='created_date', column_name="Date d'Ajout")

    class Meta:
        model = VenteModel
        fields = ['produit__shop__name', 'produit__name', 'price', 'quantity', 'price_total', 'client__fname', 'client__lname', 'client__numero', 'client__email', 'acompte', 'created_date']


class ClientExcel(resources.ModelResource):
    shop__name = Field(attribute='shop__name', column_name='Boutique')
    fname = Field(attribute='fname', column_name='Prenom')
    lname = Field(attribute='lname', column_name='Nom')
    vente_or_achat = Field(attribute='vente_or_achat', column_name='Client')
    address = Field(attribute='address', column_name='Adresse')
    age = Field(attribute='age', column_name='Age')
    nationality = Field(attribute='nationality', column_name='Nationalite')
    numero = Field(attribute='numero', column_name='Numero Telephone')
    email = Field(attribute='email', column_name='Email')
    id_card = Field(attribute='id_card', column_name="N Carte d'identite")
    created_date = Field(attribute='created_date', column_name="Date d'Ajout")

    class Meta:
        model = ClientModel
        fields =['shop__name', 'fname', 'lname', 'vente_or_achat', 'address', 'age', 'nationality', 'numero', 'email', 'id_card', 'created_date']