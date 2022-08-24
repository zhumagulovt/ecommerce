from django.db.models import Avg
from django.contrib import admin

from admin_numeric_filter.admin import RangeNumericFilter

from .models import Product, Category, ProductImage, Article, Rating

admin.site.register(Rating)


class CustomRangeNumericFilter(RangeNumericFilter):
    template = "products/admin/filter_numeric_range.html"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    fields = ('name',)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    max_num = 10
    verbose_name = "Фото товара"
    verbose_name_plural = "Фото товаров"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'amount',
                    'sold', 'created_at', 'updated_at', 'average_rating')

    list_display_links = ('id',)
    search_fields = ('name',)
    list_editable = ('name', 'category', 'price', 'amount')
    list_filter = (
        'category', 
        ('price', CustomRangeNumericFilter),
        'created_at', 
        'updated_at')
    # Product.objects.annotate(average_ratings = Avg('ratings__rating')).order_by('-average_ratings')
    inlines = (ProductImageAdmin,)

    def average_rating(self, obj):
        return obj.ratings.aggregate(Avg('rating'))['rating__avg']

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        qs = qs.annotate(Avg('ratings__rating'))
        return qs

    average_rating.admin_order_field = 'ratings__rating__avg'
    average_rating.short_description = 'Рейтинг'

admin.site.register(Article)