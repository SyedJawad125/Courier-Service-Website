from django_filters import DateFilter, CharFilter, FilterSet # type: ignore
from .models import *


class UserFilter(FilterSet):
    guid = CharFilter(field_name='guid')
    date_from = DateFilter(field_name='created_at', lookup_expr='gte' )
    date_to = DateFilter(field_name='created_at', lookup_expr='lte' )
    username = CharFilter(field_name='username', lookup_expr='icontains')
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    dept_location = CharFilter(field_name='dept_location', lookup_expr='icontains')

    class Meta:
        model = User
        fields ='__all__'