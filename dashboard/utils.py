import json
import pandas as pd
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from django.db.models import Q
from functools import reduce

# For rendering a pdf File
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from collections import OrderedDict

import datetime
from collections import OrderedDict
months = ['January','February','March','April','May','June','July','August','September','October','November','December',]
class Utils:

    '''

    '''

    def benefice_per_day(self, db_vente, db_produit, is_superuser=True, user=None):
        """
        Calculate the Total benefice of the Shop:
            db_vente : is the Sales Model object (VenteModel)
            db_depot : is the Depot Vente Model object (DepotVenteModel)
            db_achat : is the total sum of all Achat Direct Model (AchatDirectModel)
        """
        # today day
        today = datetime.date.today()
        if is_superuser:
            vente = db_vente.objects.filter(created_date__day=today.day)
            achat = db_produit.objects.filter(created_date__day=today.day)
        else:
            vente = db_vente.objects.filter(created_date__day=today.day, produit__shop__owner__user=user)
            achat = db_produit.objects.filter(created_date__day=today.day, shop__owner__user=user)

        sum_vente = sum(
            [v.price_total for v in vente if v.price_total != None])
        sum_achat = sum(
            [a.price_total_tt_produit for a in achat if a.price_total_tt_produit != None])
        return (sum_vente - sum_achat)

    def benefice_per_month(self, db_vente, db_produit, is_superuser=True, user=None):
        """
        Calculate the Total benefice of the Shop:
            db_vente : is the Sales Model object (VenteModel)
            db_depot : is the Depot Vente Model object (DepotVenteModel)
            db_achat : is the total sum of all Achat Direct Model (AchatDirectModel)
        """
        today = datetime.date.today()
        if is_superuser:
            vente = db_vente.objects.filter(created_date__month=today.month)
            achat = db_produit.objects.filter(created_date__month=today.month)
        else:
            vente = db_vente.objects.filter(created_date__month=today.month, produit__shop__owner__user=user)
            achat = db_produit.objects.filter(created_date__month=today.month, shop__owner__user=user)
        sum_vente = sum(
            [v.price_total for v in vente if v.price_total != None])
        sum_achat = sum(
            [a.price_total_tt_produit for a in achat if a.price_total_tt_produit != None])
        return (sum_vente - sum_achat)

    def benefice_vente(self, db_vente, db_produit , is_superuser=True, user=None):
        """
        Calculate the Total benefice of the Shop:
            db_a_direct : is the Achat Direct Model object (DepositStockModel)
            db_dvs : is the Depot Vente Model object (DepotVenteStockModel)
            sales : is the total sum of all sales 
        """
        if is_superuser:
            vente = db_vente.objects.all()
            achat = db_produit.objects.all()
        else:
            vente = db_vente.objects.filter(produit__shop__owner__user=user)
            achat = db_produit.objects.filter(shop__owner__user=user)
        sum_vente = sum(
            [v.price_total for v in vente if v.price_total != None])
        sum_achat = sum(
            [a.price_total_tt_produit for a in achat if a.price_total_tt_produit != None])
        return (sum_vente - sum_achat)

    def chartObject(self, db, key=None, dv_or_ad=None, dt_col_name=None, uname=None, is_superuser=True):
        # Let's check is user is superuser or not
       
        if is_superuser:
            if dv_or_ad:
                df = pd.DataFrame(db.objects.filter(
                    dv_or_ad=dv_or_ad).values())
            else:
                df = pd.DataFrame(db.objects.all().values())
        else:
            if dv_or_ad:
                df = pd.DataFrame(db.objects.filter(
                    shop__owner__user__username=uname, dv_or_ad=dv_or_ad).values())
            else:
                df = pd.DataFrame(db.objects.filter(
                    shop__owner__user__username=uname).values())
        
        if not df.empty:
            un_x = df.groupby(
                df[dt_col_name].dt.strftime('%B')).agg({key: 'sum'})
            # Parsed it
            monthtly_data = json.loads(un_x.to_json())
            # the monthly key
            msp = monthtly_data[key]
            msp= OrderedDict(sorted(msp.items(),key =lambda x:months.index(x[0])))
            # print(msp)

            dataset = { 'months': [m for m in msp.keys()], 
                        'data': [d for d in msp.values()]}
            # print(type(dataset))
            # print((dataset))

        else:
            dataset = {'months': ['Jan', 'Fev', 'Avr'],
                       'data': [0, 0, 0]}

        return mark_safe(escapejs(json.dumps(dataset)))

    def label_notif_as_read(self, obj):
        notifs = obj.objects.filter(read=False)
        for notif in notifs:
            notif.read = True
            notif.save()
        return

    def chart_client(self, db, key=None, dt_col_name=None, uname=None, is_superuser=True):
        # Let's check is user is superuser or not
        if is_superuser:
            df = pd.DataFrame(db.objects.all().values())
        else:
            df = pd.DataFrame(db.objects.filter(
                shop__owner__user__username=uname).values())
        if not df.empty:
            un_x = df.groupby(
                df[dt_col_name].dt.strftime('%B')).agg({key: 'sum'})
            # Parsed it
            monthtly_data = json.loads(un_x.to_json())
            # the monthly key
            msp = monthtly_data[key]
            msp= OrderedDict(sorted(msp.items(),key =lambda x:months.index(x[0])))
            dataset = { 'months': [m for m in msp.keys()], 
                        'data': [d for d in msp.values()]}

        else:
            dataset = {'months': ['Jan', 'Fev', 'Avr'],
                       'data': [0, 0, 0]}

        return mark_safe(escapejs(json.dumps(dataset)))

    def chart_vente(self, db, key=None, dt_col_name=None, uname=None, is_superuser=True):
        # Let's check is user is superuser or not
        if is_superuser:
            df = pd.DataFrame(db.objects.all().values())
        else:
            df = pd.DataFrame(db.objects.filter(
                produit__shop__owner__user__username=uname).values())
        if not df.empty:
            un_x = df.groupby(
                df[dt_col_name].dt.strftime('%B')).agg({key: 'sum'})
            # Parsed it
            monthtly_data = json.loads(un_x.to_json())
            # the monthly key
            msp = monthtly_data[key]
            msp= OrderedDict(sorted(msp.items(),key =lambda x:months.index(x[0])))
            dataset = {'months': [m for m in msp.keys()], 'data': [
                d for d in msp.values()]}
            
        else:
            dataset = {'months': ['Jan', 'Fev', 'Avr'],
                       'data': [0, 0, 0]}

        return mark_safe(escapejs(json.dumps(dataset)))

    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    

    def product_filter(self, products, paramDict):
        # paramDict = request.GET
        params = paramDict.keys()
 
        # data filtering
        if any(x!='' for x in paramDict.values()):

            # filters records that contain any of the following keywords
            if paramDict.get('search', '') != '':
                kws = paramDict['search'].split()
                q_lookups = [Q(name__icontains=kw) for kw in kws] 
                            # [Q(street__icontains=kw) for kw in kws] + \
                            # [Q(town__icontains=kw) for kw in kws]
                filters = Q()
                filters |= reduce(lambda x, y: x | y, q_lookups)
                products = products.filter(filters)

        return products


class RedirectToPreviousMixin:
    '''
        This class allows to make redirection to previous
        page.
    '''

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get(
            'HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']

    # benefice par mois

    def benefice_per_month(self, db_vente, db_depot, db_achat):
        """
        Calculate the Total benefice of the Shop:
            db_vente : is the Sales Model object (VenteModel)
            db_depot : is the Depot Vente Model object (DepotVenteModel)
            db_achat : is the total sum of all Achat Direct Model (AchatDirectModel) 
        """
        today = datetime.date.today()
        vente = db_vente.objects.filter(mydatefield__year=today.year,
                                        mydatefield__month=today.month)
        depot = db_depot.objects.filter(mydatefield__year=today.year,
                                        mydatefield__month=today.month)
        achat = db_achat.objects.filter(mydatefield__year=today.year,
                                        mydatefield__month=today.month)

        sum_vente = sum(
            [p.price_total for p in vente if p.price_total != None])
        sum_depot = sum(
            [p.produit.price_total for p in depot if p.produit.price_total != None])
        sum_achat = sum(
            [p.produit.price_total for p in achat if p.produit.price_total != None])
        return (sum_vente - (sum_depot + sum_achat))
