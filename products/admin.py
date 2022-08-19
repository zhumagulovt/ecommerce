from django.contrib import admin

from .models import Product, Category, ProductImage, Article

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
                    'sold', 'created_at', 'updated_at', 'get_average_rating')

    list_display_links = ('id', 'name')
    list_filter = ('category',)
    inlines = (ProductImageAdmin,)


admin.site.register(Article)