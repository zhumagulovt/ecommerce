from django.db.models import Avg
from django.contrib import admin
from django.db.models.fields import DecimalField, FloatField, IntegerField, AutoField

from .models import Product, Category, ProductImage, Article, Rating
from .forms import RangeNumericForm

admin.site.register(Rating)


class RangeNumericFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = "products/admin/filter_numeric_range.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if not isinstance(field, (DecimalField, IntegerField, FloatField, AutoField)):
            raise TypeError('Class {} is not supported for {}.'.format(type(self.field), self.__class__.__name__))

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + '_from' in params:
            value = params.pop(self.field_path + '_from')
            self.used_parameters[self.field_path + '_from'] = value

        if self.parameter_name + '_to' in params:
            value = params.pop(self.field_path + '_to')
            self.used_parameters[self.field_path + '_to'] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            filters.update({
                self.parameter_name + '__gte': self.used_parameters.get(self.parameter_name + '_from', None),
            })

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            filters.update({
                self.parameter_name + '__lte': self.used_parameters.get(self.parameter_name + '_to', None),
            })

        return queryset.filter(**filters)

    def expected_parameters(self):
        return [
            '{}_from'.format(self.parameter_name),
            '{}_to'.format(self.parameter_name),
        ]

    def choices(self, changelist):
        return ({
            'request': self.request,
            'parameter_name': self.parameter_name,
            'form': RangeNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', None),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', None),
            }),
        }, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    fields = ('name',)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    max_num = 10
    verbose_name = "Фото товара"
    verbose_name_plural = "Фото товаров"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_select_related = True
    # raw_id_fields = ['category']
    list_display = ('id', 'name', 'category', 'price', 'amount',
                    'sold', 'created_at', 'updated_at', #'average_rating'
                    )

    list_display_links = ('id',)
    search_fields = ('name',)
    list_editable = ('name', 'price', 'amount')
    list_filter = (
        'category', 
        ('price', RangeNumericFilter),
        'created_at', 
        'updated_at')
    
    # Product.objects.annotate(average_ratings = Avg('ratings__rating')).order_by('-average_ratings')
    inlines = (ProductImageAdmin,)

    # def average_rating(self, obj):
    #     return obj.ratings.aggregate(Avg('rating'))['rating__avg']

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request).select_related('category')
        # qs = qs.annotate(Avg('ratings__rating'))
        return qs

    # average_rating.admin_order_field = 'ratings__rating__avg'
    # average_rating.short_description = 'Рейтинг'

admin.site.register(Article)