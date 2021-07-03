import json
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from django import template 
from dashboard.models import ProductModel

register = template.Library()

@register.simple_tag
def list_item(context):
    user = context['request'].user
    if user.is_superuser:
        products = ProductModel.objects.all()
    else:
        products = ProductModel.objects.filter(shop__owner__user=user)
    r = { p.name: p.pk for p in products }
    r_json = json.dumps(r)
    return mark_safe(escapejs(r_json))

list_item = register.simple_tag(takes_context=True)(list_item)
