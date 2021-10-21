from django.shortcuts import render
from dashboard.forms import ProductModelForm
from dashboard.models import ProductModel
from dashboard.utils import Utils
from django.core.paginator import Paginator
from django.utils.encoding import iri_to_uri

from search.filter import advanced_filter


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


def advanced_search_view(request):

    products = ProductModel.objects.all()
    form = ProductModelForm(request.GET or None)

    if request.method == 'GET':
        paramDict = request.GET 
        products = advanced_filter(products, paramDict)

        # Paginate results
        products = Paginator(products, 10)

    context = {
        'products': products,
        'form': form
    }

    return render(request, 'search/advanced_search.html', context)
