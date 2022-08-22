from django.db.models import Avg

from rest_framework import serializers

from .models import (
    Article, 
    Product, 
    Category, 
    ProductImage, 
    Comment, 
    Rating,
    Like
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
        fields = "__all__"


class CommentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for comment update, to make only 'content' field editable"""

    class Meta:
        model = Comment
        fields = ['content']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for rating"""

    class Meta:
        model = Rating
        exclude = ['product']


class RatingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for rating update, to make only 'rating' field editable"""

    class Meta:
        model = Rating
        fields = ['rating']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail product with all related fields"""

    images = ProductImageSerializer(read_only=True, many=True)
    rated = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
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
            'rated',
            'average_rating',
            'is_liked',
            'likes_count',
            'images',
            'comments_count',
            'comments'
        ]

    def get_rated(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            if Rating.objects.filter(user=user, product=obj).exists():
                return Rating.objects.get(user=user, product=obj).rating
        return None

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            if Like.objects.filter(user=user, product=obj).exists():
                return True
        return False

    def get_likes_count(self, obj):
        return obj.likes.count()


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for article"""

    class Meta:
        model = Article
        fields = "__all__"
