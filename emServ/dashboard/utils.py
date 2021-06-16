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

    def benefice_sale(self, db, spent):
        stocks = db.objects.all()
        sum_stocks = sum([p.prix_d_achat for p in stocks])
        return (spent - sum_stocks)
    
    def benefice(self, dbs, dbv, sales):
        """
            dbs: is the Achat Direct model object
            dbv: is the DepotVente model object
            sales: is the sum of the sale from Sale Model (BuyingStock)
        """
        stocks = dbs.objects.all()
        dvs = dbv.objects.all()
        sum_stock = sum([p.prix_d_achat for p in stocks])
        sum_dvs = sum([p.prix_d_vente for p in dvs])
        return (sales - (sum_dvs + sum_stock))

    def benefice_stock(self, db, spent):
        sales = db.objects.all()
        sum_sales = sum([p.prix_de_vente_fin for p in sales])
        return (sum_sales - spent)

    def chartObject(self, db, key=None, dt_col_name=None):
        df = pd.DataFrame(db.objects.all().values())
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