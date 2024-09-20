from django.contrib import admin
from .models import Collection,Product,Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page=10

    @admin.display(ordering='inventory')
    def inventory_status (self,product):
        if product.inventory <10:
             return 'Low'
        return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_per_page=10
    list_editable=['membership']

# Register your models here.
admin.site.register(Collection)
# admin.site.register(Product,ProductAdmin)
admin.site.register(Customer,CustomerAdmin)