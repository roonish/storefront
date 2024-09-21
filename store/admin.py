from itertools import count
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from .models import Collection,Product,Customer,Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection','last_update']

    def collection_title(self,product):
        return product.collection.title
        

    @admin.display(ordering='inventory')
    def inventory_status (self,product):
        if product.inventory <10:
             return 'Low'
        return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    #for form change fields,except,readonly ,pre populated field,
    fields = ['first_name']
    list_display = ['first_name','last_name','membership']
    list_per_page=10
    list_editable=['membership']
    ordering = ['first_name','last_name']
    #startswith search name whose first letter match. to make it case insensetive we can also add i . so istartswith
    search_fields=['first_name__istartswith','last_name__istartswith']

class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self,collection):
        return collection.product_count
    
    #to override base queryset
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(product_count=Count('product'))

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','customer','placed_at']

# Register your models here.
admin.site.register(Collection,CollectionAdmin)
# admin.site.register(Product,ProductAdmin)
admin.site.register(Customer,CustomerAdmin)