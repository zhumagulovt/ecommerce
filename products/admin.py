from django.contrib import admin

from .models import Product, Category, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_new', 'created_at', 'updated_at')
    list_editable = ('is_new',)
    list_display_links = ('id', 'name')
    list_filter = ('category',)
