from django.contrib import admin

from .models import Product, Category, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    fields = ('name',)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    max_num = 10
    verbose_name = "Фото товара"
    verbose_name_plural = "Фото товаров"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_new', 'created_at', 'updated_at')
    list_editable = ('is_new',)
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    inlines = (ProductImageAdmin,)