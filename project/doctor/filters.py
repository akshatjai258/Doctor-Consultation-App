import django_filters
from django_filters import CharFilter
from django.contrib.auth.models import User
from .models import Doctor
class search_user(django_filters.FilterSet):
    class Meta:
        model=User
        fields = ['username']
        


class search_doctor(django_filters.FilterSet):
    Address=CharFilter(field_name='Address',lookup_expr='icontains')
    class Meta:
        model=Doctor
        fields = ['user','specialization','state','Address']

        