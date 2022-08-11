from itertools import product
from django.views.generic import ListView

from .models import Category, Product


class ProductListView(ListView):
    model = Product


class ProductCategoryListView(ListView):
    model = product

    def get_queryset(self):
        category = Category.objects.get(slug = self.kwargs.get('slug'))
        return category.product_set.all()