from extra_views import InlineFormSetFactory
from django.forms import fields, forms
from django.forms.models import inlineformset_factory

from .models import (   ProductModel, 
                        DepositStockModel,
                        BuyingStockModel,
                        ClientModel,
                        ClientRequestModel
)

# ProductDepositFormset = inlineformset_factory(
#                                                 ProductModel, 
#                                                 DepositStockModel, 
#                                                 fields='__all__',
#                                                 max_num=1,
#                                                 can_delete=True
#                                             )

class ProductDepositInline(InlineFormSetFactory):

    model = ProductModel
    fields = '__all__'


class DepositStockInline(InlineFormSetFactory):

    model = DepositStockModel
    fields = '__all__'