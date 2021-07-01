from django import template 
from dashboard.models import ProductModel

register = template.Library()

@register.inclusion_tag('dashboard/inclusions/product_detail.html')
def render_product_detail(pk):
    return {
        'productDetail': ProductModel.objects.get(pk=pk)
    }
    