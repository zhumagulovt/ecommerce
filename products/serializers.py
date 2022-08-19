from django.db.models import Avg

from rest_framework import serializers

from .models import (
    Article, 
    Product, 
    Category, 
    ProductImage, 
    Comment, 
    Rating
)

from users.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for image of product"""

    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product in list"""

    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        img = obj.images.all()[:1]
        if img.exists():
            return ProductImageSerializer(img[0]).data
        # return {image: null}
        return None


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category"""

    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['id', 'product']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for rating"""

    class Meta:
        model = Rating
        exclude = ['product']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail product with all related fields"""

    images = ProductImageSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'amount',
            'sold',
            'created_at',
            'updated_at',
            'category',
            'average_rating',
            'likes_count',
            'images',
            'comments_count',
            'comments'
        ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for article"""

    class Meta:
        model = Article
        fields = "__all__"
