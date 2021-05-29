from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, "dashboard/index.html", {})



def profile(request):
    """
        Fonction    : Profile Utilisateur
        Model       : - User
                      - Profile
        Context     : 
    """

    return render(request, "dashboard/profile.html", {})



def client(request):
    """
        Fonction    : Gestion de Client
        Model       : - ClientModel

        Context     : 
    """

    return render(request, "dashboard/client.html", {})



def clientRequest(request):
    """
        Fonction    : Demande Client
        Model       : - ClientRequestModel
                      - ClientModel  
        Context     : 
    """

    return render(request, "dashboard/client_request.html", {})



def depositStock(request):
    """
        Fonction    : Stock Depot
        Model       : - DepositStockModel

        Context     : 
    """

    return render(request, "dashboard/deposit.html", {})




def buyingStock(request):
    """
        Fonction    : Stock Achat
        Model       : - BuyingStockModel

        Context     : 
    """

    return render(request, "dashboard/buying.html", {})




def product(request):
    """
        Fonction    : Produit
        Model       : - ProdcutModel

        Context     : 
    """

    return render(request, "dashboard/produit.html", {})