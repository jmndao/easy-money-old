import json
import pandas as pd
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

# For rendering a pdf File
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import datetime


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
            [a.price_total for a in achat if a.price_total != None])
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
            [a.price_total for a in achat if a.price_total != None])
        return (sum_vente - sum_achat)

    def benefice_vente(self, db_a_direct, db_dvs, sales):
        """
        Calculate the Total benefice of the Shop:
            db_a_direct : is the Achat Direct Model object (DepositStockModel)
            db_dvs : is the Depot Vente Model object (DepotVenteStockModel)
            sales : is the total sum of all sales 
        """
        a_directs = db_a_direct.objects.all()
        dvs = db_dvs.objects.all()
        sum_a_directs = sum(
            [p.produit.price_total for p in a_directs if p.produit.price_total != None])
        sum_dvs = sum(
            [p.produit.price_total for p in dvs if p.produit.price_total != None])
        return (sales - (sum_a_directs + sum_dvs))

    def benefice_depot_vente(self, db_a_direct, db_sales, dv):
        """
        Calculate the Total benefice of the Shop:
            db_a_direct: is the Achat Direct model object
            db_sales: is the BuyingStock model object
            dv: is the sum of the depot vente from DepotVenteStockModel
        """
        a_directs = db_a_direct.objects.all()
        sales = db_sales.objects.all()
        sum_a_directs = sum([p.price for p in a_directs if p.price != None])
        sum_sales = sum([p.price for p in sales if p.price != None])
        return (sum_sales - (dv + sum_a_directs))

    def benefice_achat_direct(self, db_sales, db_dvs, d_stock):
        """
        Calculate the Total benefice of the Shop:
            db_sales : is the Sales Model object (BuyingStockModel)
            db_dvs : is the Depot Vente Model object (DepotVenteStockModel)
            d_stock : is the total sum of all Achat Direct Model (DepositStockModel) 
        """
        sales = db_sales.objects.all()
        dvs = db_dvs.objects.all()
        sum_sales = sum([p.price for p in sales if p.price != None])
        sum_dvs = sum([p.price for p in dvs if p.price != None])
        return (sum_sales - (d_stock + sum_dvs))

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
        print(df)
        if not df.empty:
            un_x = df.groupby(
                df[dt_col_name].dt.strftime('%B')).agg({key: 'sum'})
            # Parsed it
            monthtly_data = json.loads(un_x.to_json())
            # the monthly key
            msp = monthtly_data[key]
            dataset = { 'months': [m for m in msp.keys()], 
                        'data': [d for d in msp.values()]}

        else:
            dataset = {'months': ['Jan', 'Fev', 'Avr'],
                       'data': [0, 0, 0]}
        print(dataset)

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
