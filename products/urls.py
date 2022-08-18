from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('<slug:slug>/', views.ProductCategoryListView.as_view())
]