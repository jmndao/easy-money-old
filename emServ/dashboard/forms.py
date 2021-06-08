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
