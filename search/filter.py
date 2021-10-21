from decimal import Decimal
from functools import reduce
from django.db.models import Q
# from dashboard.models import ProductModel



def advanced_filter(products, paramDict, prange):
    """
        This function implement advanced research for products.
        It searches a product by 
            - name 
            - category  : Select List
            - client : Select List
            - quantity
            - depot vente / achat : Select List
            - price range
            ------------ Select List  
            - dimension 
            - estate 
            - obsolescence,
            - rarety 
            ------------ End Select List
            - disk memory 
            - ram memory 
            - model 
            - year 
            - color 
            - matter 
            - description
            ------------ Checkbox
            - charger 
            - original box 
            - bill 
            - guaranteed 
            - connectics.
            ------------ End Checkbox
    """

    # paramDict = request.GET
    params = paramDict.keys()

    # data filtering
    if any(x!='' for x in paramDict.values()):

        if paramDict.get('status', '') != '':
            status = paramDict['status']
            products = products.filter(status=status)

        if prange:
            if paramDict.get('min', '') != '':
                _min = Decimal(paramDict.get('min', '').strip(' "'))
                products = products.filter(price__gte=_min)
            if paramDict.get('max', '') != '':
                _max = Decimal(paramDict.get('max', '').strip(' "'))
                products = products.filter(price__lte=_max)
                
        if paramDict.get('category', ''):
            category = paramDict['category']
            products = products.filter(category=category)
            
        if paramDict.get('beds', ''):
            beds = paramDict['beds']
            products = products.filter(rooms=beds)
            
        if paramDict.get('superficie', ''):
            sup = paramDict['superficie']
            products = products.filter(rooms__lte=sup)
            
        if paramDict.get('max_price', ''):
            _max = Decimal(paramDict.get('max_price', '').strip(' "'))
            products = products.filter(items__price__lte=_max)

        # filters records that contain any of the following keywords

        if paramDict.get('location', '') != '':
            kws = paramDict['location'].split()
            q_lookups = [Q(region__icontains=kw) for kw in kws] + \
                        [Q(street__icontains=kw) for kw in kws] + \
                        [Q(town__icontains=kw) for kw in kws]
            filters = Q()
            filters |= reduce(lambda x, y: x | y, q_lookups)
            products = products.filter(filters)

        # filters records that contain any of the following keywords
        if paramDict.get('area', '') != '':
            kws = paramDict['area'].split()
            q_lookups = [Q(region__icontains=kw) for kw in kws] + \
                        [Q(street__icontains=kw) for kw in kws] + \
                        [Q(town__icontains=kw) for kw in kws]
            filters = Q()
            filters |= reduce(lambda x, y: x | y, q_lookups)
            products = products.filter(filters)

    return products