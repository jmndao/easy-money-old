from import_export import resources
from dashboard.models import ProductModel, VenteModel, ClientModel

class ProductExcel(resources.ModelResource):
    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'dv_or_ad', 'quantity', 'shop__owner__user__username', 'montant_restauration', 'created_date']


class VenteExcel(resources.ModelResource):

    class Meta:
        model = VenteModel
        fields = ['produit__name', 'price', 'price_total', 'acompte', 'restant_du', 'quantity', 'client__fname', 'client__lname', 'quantity', 'created_date']


class ClientExcel(resources.ModelResource):

    class Meta:
        model = ClientModel
        fields =['shop__owner__user__username', 'fname', 'lname', 'sexe', 'numero', 'created_date']