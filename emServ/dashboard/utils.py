import json
import pandas as pd
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

# For rendering a pdf File
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from collections import OrderedDict

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
            dataset = { 'months': [m for m in msp.keys()], 
                        'data': [d for d in msp.values()]}

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
            msp
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

    def estimation_from_model(self, db_estimation, last=False, pk=None):
        if last:
            my_estimation = db_estimation.objects.last()
        else:
            my_estimation = db_estimation.objects.get(pk=pk)
        i_price = float(my_estimation.used_price)
        repair_amount = float(my_estimation.reparatinon_price)

        if my_estimation.estate == 'POUR_PIECE' and my_estimation.category == 'TABLETTE':
            i_price = 3000
            return  i_price

        if my_estimation.estate == 'POUR_PIECE' and my_estimation.category == 'TELEPHONE' or 'ORDINATEUR' or 'TELEVISION':
            i_price = 5000
            return  i_price
        
        percentage_1 = 0
        if my_estimation.estate == 'NEUF':
            percentage_1 = 0
        elif my_estimation.estate == 'BON':
            percentage_1 = 0.05
        elif my_estimation.estate == 'MOYEN':
            percentage_1 = 0.1
        elif my_estimation.estate == 'MAUVAIS':
            percentage_1 = 0.2
        else:
            percentage_1 = 1

        i_price = i_price - i_price * percentage_1
        percentage_2 = 0
        if my_estimation.obsolescence == 'LENTE':
            percentage_2 = 0
        elif my_estimation.obsolescence == 'MOYENNE':
            percentage_2 = 0.05
        elif my_estimation.obsolescence == 'RAPIDE':
            percentage_2 = 0.1
        elif my_estimation.obsolescence == 'TRES_RAPIDE':
            percentage_2 = 0.2
        else:
            percentage_2 = 1
        i_price = i_price - i_price * percentage_2

        percentage_3 = 0
        if my_estimation.rarety == 'RARE':
            percentage_3 = 0
        elif my_estimation.rarety == 'COURANT':
            percentage_3 = 0.05
        elif my_estimation.rarety == 'TRES_COURANT':
            percentage_3 = 0.1
        else:
            percentage_3 = None
        i_price = i_price - i_price * percentage_3

        percentage_4 = 0
        if my_estimation.original_box == True:
            percentage_4 = 0
        else:
            percentage_4 = 0.05

        i_price = i_price - i_price * percentage_4

        percentage_5 = 0
        if my_estimation.charger == 'OUI':
            percentage_5 = 0
        elif my_estimation.charger == 'NON':
            percentage_5 = 0.05
        elif my_estimation.charger == 'PAS_BESOIN':
            percentage_5 = 0
        else:
            percentage_5 = 0
        i_price = i_price - i_price * percentage_5

        percentage_6 = 0
        if my_estimation.sale_bill == True:
            percentage_6 = 0
        else:
            percentage_6 = 0.05
        i_price = i_price - i_price * percentage_6

        percentage_7 = 0
        if my_estimation.dimension == 'PETIT':
            percentage_7 = 0
        elif my_estimation.dimension == 'MOYEN':
            percentage_7 = 0.05
        elif my_estimation.dimension == 'GRAND':
            percentage_7 = 0.1
        else:
            percentage_7 = None
        i_price = i_price - i_price * percentage_7

        i_price = i_price - repair_amount

        percentage_8 = 0.02
        
        diff_year = int(my_estimation.created_date.year) - int(my_estimation.year_of_release)
        assert diff_year > 0

        i_price = i_price - i_price * diff_year * percentage_8

        print(diff_year)
        return int(i_price)

    def estimation_from_form(self, form):
        
        i_price = form.instance.used_price = float(form.instance.new_price) // 2
        repair_amount = float(form.instance.reparatinon_price)

        percentage_1 = 0
        if form.instance.estate == 'NEUF':
            percentage_1 = 0
        elif form.instance.estate == 'BON':
            percentage_1 = 0.05
        elif form.instance.estate == 'MOYEN':
            percentage_1 = 0.1
        elif form.instance.estate == 'MAUVAIS':
            percentage_1 = 0.2
        else:
            percentage_1 = 1

        i_price = i_price - i_price * percentage_1
        percentage_2 = 0
        if form.instance.obsolescence == 'LENTE':
            percentage_2 = 0
        elif form.instance.obsolescence == 'MOYENNE':
            percentage_2 = 0.05
        elif form.instance.obsolescence == 'RAPIDE':
            percentage_2 = 0.1
        elif form.instance.obsolescence == 'TRES_RAPIDE':
            percentage_2 = 0.2
        else:
            percentage_2 = None
        i_price = i_price - i_price * percentage_2

        percentage_3 = 0
        if form.instance.rarety == 'RARE':
            percentage_3 = 0
        elif form.instance.rarety == 'COURANT':
            percentage_3 = 0.05
        elif form.instance.rarety == 'TRES_COURANT':
            percentage_3 = 0.1
        else:
            percentage_3 = None

        i_price = i_price - i_price * percentage_3

        percentage_4 = 0
        if form.instance.original_box == True:
            percentage_4 = 0
        else:
            percentage_4 = 0.05

        i_price = i_price - i_price * percentage_4

        percentage_5 = 0
        if form.instance.charger == 'OUI':
            percentage_5 = 0
        elif form.instance.charger == 'NON':
            percentage_5 = 0.05
        elif form.instance.charger == 'PAS_BESOIN':
            percentage_5 = 0
        else:
            percentage_5 = 0
        i_price = i_price - i_price * percentage_5

        percentage_6 = 0
        if form.instance.sale_bill == True:
            percentage_6 = 0
        else:
            percentage_6 = 0.05
        i_price = i_price - i_price * percentage_6

        percentage_7 = 0
        if form.instance.dimension == 'PETIT':
            percentage_7 = 0
        elif form.instance.dimension == 'MOYEN':
            percentage_7 = 0.05
        elif form.instance.dimension == 'GRAND':
            percentage_7 = 0.1
        else:
            percentage_7 = None
        i_price = i_price - i_price * percentage_7

        i_price = i_price - repair_amount
        return int(i_price)


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
