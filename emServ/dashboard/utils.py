import json
import pandas as pd
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

# For rendering a pdf File
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa




class Utils:

    '''
        
    '''

        
    def benefice_sale(self, db_a_direct, db_dvs, sales):
        """
        Calculate the Total benefice of the Shop:
            db_a_direct : is the Achat Direct Model object (DepositStockModel)
            db_dvs : is the Depot Vente Model object (DepotVenteStockModel)
            sales : is the total sum of all sales 
        """
        a_directs = db_a_direct.objects.all()
        dvs = db_dvs.objects.all()
        sum_a_directs = sum([p.prix_d_achat for p in a_directs])
        sum_dvs = sum([p.prix_d_depot for p in dvs])
        return (sales - (sum_a_directs + sum_dvs))
    
    def benefice_dv(self, db_a_direct, db_sales, dv):
        """
        Calculate the Total benefice of the Shop:
            db_a_direct: is the Achat Direct model object
            db_sales: is the BuyingStock model object
            dv: is the sum of the depot vente from DepotVenteStockModel
        """
        a_directs = db_a_direct.objects.all()
        sales = db_sales.objects.all()
        sum_a_directs = sum([p.prix_d_achat for p in a_directs])
        sum_sales = sum([p.prix_d_vente_fin for p in sales])
        return (sum_sales - (dv + sum_a_directs))

    def benefice_stock(self, db_sales, db_dvs, d_stock):
        """
        Calculate the Total benefice of the Shop:
            db_sales : is the Sales Model object (BuyingStockModel)
            db_dvs : is the Depot Vente Model object (DepotVenteStockModel)
            d_stock : is the total sum of all Achat Direct Model (DepositStockModel) 
        """
        sales = db_sales.objects.all()
        dvs = db_dvs.objects.all()
        sum_sales = sum([p.prix_de_vente_fin for p in sales])
        sum_dvs = sum([p.prix_d_depot for p in dvs])
        return (sum_sales - (d_stock + sum_dvs))

    def chartObject(self, db, key=None, dt_col_name=None):
        df = pd.DataFrame(db.objects.all().values())
<<<<<<< HEAD
        un_x = df.groupby(df[dt_col_name].dt.strftime('%B')).agg({key : 'sum'})
        # Parsed it 
        monthtly_data = json.loads(un_x.to_json())
        # the monthly key
        msp = monthtly_data[key]
        dataset = {'months':[m for m in msp.keys()], 'data':[d for d in msp.values()]}
        return mark_safe(escapejs(json.dumps(dataset)))
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
=======
        if not df.empty:
            un_x = df.groupby(df[dt_col_name].dt.strftime('%B')).agg({key : 'sum'})
            # Parsed it 
            monthtly_data = json.loads(un_x.to_json())
            # the monthly key
            msp = monthtly_data[key]
            dataset = {'months':[m for m in msp.keys()], 'data':[d for d in msp.values()]}
            #return mark_safe(escapejs(json.dumps(dataset)))
        else:
           dataset = {   'months': ['Jan', 'Fev', 'Avr'],
                            'data': [10, 12, 8]   }

        return mark_safe(escapejs(json.dumps(dataset)))
>>>>>>> 850754e40547895ca97bc117b9300603869b3727
