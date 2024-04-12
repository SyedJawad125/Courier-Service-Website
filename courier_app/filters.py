from django_filters import DateFilter, CharFilter, FilterSet
from .models import *


class ProductFilter(FilterSet):
    id = CharFilter(field_name='id')
    # dept_updated_by_user= CharFilter(field_name='id')
    # dept_added_by_user= CharFilter(field_name='id')
    date_from = DateFilter(field_name='created_at', lookup_expr='gte' )
    date_to = DateFilter(field_name='created_at', lookup_expr='lte' )
    name = CharFilter(field_name='name', lookup_expr='icontains')
    price = CharFilter(field_name='price')
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields ='__all__'


class OrderFilter(FilterSet):
    id = CharFilter(field_name='id')
    # dept_updated_by_user= CharFilter(field_name='id')
    # dept_added_by_user= CharFilter(field_name='id')
    date_from = DateFilter(field_name='created_at', lookup_expr='gte' )
    date_to = DateFilter(field_name='created_at', lookup_expr='lte' )
    delivery_address = CharFilter(field_name='delivery_address', lookup_expr='icontains')
    bill = CharFilter(field_name='bill')

    class Meta:
        model = Order
        fields ='__all__'
