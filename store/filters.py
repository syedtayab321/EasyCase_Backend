from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'collection_id': ['exact'],
      'brand': ['exact'],
      'model': ['exact'],
      'unit_price': ['gt', 'lt']
    }