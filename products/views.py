from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status, mixins
from rest_framework.pagination import PageNumberPagination

from .models import Article, Category, Comment, Product, Rating, Like
from .permissions import IsOwner
from .serializers import (
    ArticleSerializer, 
    CategorySerializer,
    CommentSerializer,
    CommentUpdateSerializer,
    RatingSerializer,
    RatingUpdateSerializer,
    ProductSerializer, 
    ProductDetailSerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 50
    # page_query_param = 'p'


class LatestProductList(APIView):
    """Last added products"""

    def get(self, request):
        products = Product.objects.all().prefetch_related('images')[:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(RetrieveAPIView):
    """View for product detail"""

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
# class ProductDetail(APIView):

#     def get_object(self, pk):
#         product = get_object_or_404(Product, pk=pk)
#         return product

#     def get(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

class CategoryList(ListAPIView):
    """List of categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class ProductListByCategory(APIView):
#     """List of products by category"""
#     pagination_class = CustomPagination

#     def get(self, request, slug):
#         products = Product.objects.filter(
#             category__slug=slug
#         ).prefetch_related('images').select_related('category')

#         serializer = ProductSerializer(products, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListByCategory(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(
            category__id=self.kwargs.get('pk')
        ).prefetch_related('images').select_related('category')

        return queryset


class LatestArticleList(APIView):
    "Last added articles"

    def get(self, request):
        articles = Article.objects.order_by('-created_at')[:5]
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):

    permission_classes = [IsOwner, IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:

            return CommentUpdateSerializer
        
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingView(mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingUpdateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def get_object(self):
        return get_object_or_404(
            Rating, 
            product_id=self.kwargs['pk'],
            user=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(
            product_id=self.kwargs.get('pk'),
            user=self.request.user
        )


class LikeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        if Like.objects.filter(user=user, product=product).exists():
            Like.objects.filter(user=user, product=product).delete()
        else:
            Like.objects.create(user=user, product=product)
        
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    
    if query:   
        products = Product.objects.filter(
            Q(name__icontains=query)
        ).prefetch_related('images').select_related('category')
        print(products.query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []})