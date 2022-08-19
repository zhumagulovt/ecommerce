from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article, Category, Product
from .serializers import (
    ArticleSerializer, 
    CategorySerializer, 
    ProductSerializer, 
    ProductDetailSerializer
)


class LatestProductList(APIView):
    """Last added products"""

    def get(self, request):
        products = Product.objects.order_by('-created_at')[:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(RetrieveAPIView):
    """View for product detail"""

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CategoryList(ListAPIView):
    """List of categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListByCategory(APIView):
    """List of products by category"""

    def get(self, request, slug):
        products = Product.objects.filter(category__slug=slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LatestArticleList(APIView):
    "Last added articles"

    def get(self, request):
        articles = Article.objects.order_by('-created_at')[:5]
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
