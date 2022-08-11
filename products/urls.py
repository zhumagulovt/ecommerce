from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('<slug:slug>/', views.ProductCategoryListView.as_view())
]