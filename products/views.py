from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Category, Product, Order, OrderItem


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


class ProductCategoryListView(ListView):
    model = Product

    def get_queryset(self):
        category = Category.objects.get(slug = self.kwargs.get('slug'))
        return category.product_set.all()


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect(product.get_absolute_url())


def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        else:
            # Item isn't in order
            return redirect(product.get_absolute_url())

    else:
        # Order does not exist
        return redirect(product.get_absolute_url())

    return redirect(product.get_absolute_url())