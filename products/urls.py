from django.urls import path, include

from . import views
from .routers import router

urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('news/', views.LatestArticleList.as_view()),
    path('products/', include(router.urls)),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/<int:pk>/rating/', views.RatingView.as_view()),
    path('products/<int:pk>/like/', views.LikeView.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<slug:slug>/', views.ProductListByCategory.as_view()),
]