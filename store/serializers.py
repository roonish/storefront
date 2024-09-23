from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    #can also change name of serializer object by giving source
    price = serializers.DecimalField(max_digits=6, decimal_places=2,source = 'unit_price')
    #can also add new field which is not in db
    tax = serializers.SerializerMethodField(method_name="calculate_tax")
    #to add relationship between different model
    collection = CollectionSerializer()
    #serializers.StringRelatedField()

    def calculate_tax(self,product:Product):
        return product.unit_price*Decimal(1.1)