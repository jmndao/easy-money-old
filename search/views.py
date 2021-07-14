from django.shortcuts import render
from dashboard.models import ProductModel
from dashboard.utils import Utils

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
    return render(request, 'search/results.html', context)
