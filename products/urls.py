from django.urls import path

from . import views

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('news/', views.LatestArticleList.as_view()),
    path('p/<int:pk>/', views.ProductDetail.as_view()),
    path('<slug:slug>/', views.ProductListByCategory.as_view()),
]