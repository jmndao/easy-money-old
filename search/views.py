from django.shortcuts import render
from dashboard.models import ProductModel
from dashboard.utils import Utils
from django.utils.encoding import iri_to_uri


# Create your views here.

def search_product_view(request):

    """
        Search Product here.
    """

    utils = Utils()

    products = ProductModel.objects.all()

    paramDict = request.GET
    products = utils.product_filter(products, paramDict)

    context = {
        'products': products,
        'ncount': len(products),
        'title': "Recherche"
    }
    return render(request, iri_to_uri('search/results.html'), context)
