import django_filters
from django_filters import CharFilter
from .models import Doctor

class search_doctor(django_filters.FilterSet):
    Address=CharFilter(field_name='Address',lookup_expr='icontains')
    class Meta:
        model=Doctor
        fields = ['Address','city','country','state']