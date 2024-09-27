from rest_framework import serializers
from .models import Product,Collection,Review
from decimal import Decimal

# class CollectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ['id','title']
#     # id = serializers.IntegerField()
#     # title = serializers.CharField(max_length=255)
    

class CollectionSerializer(serializers.ModelSerializer):
        class Meta:
            model=Collection
            fields=['id','title','product_count']

        product_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['id','title','slug','description','price','inventory','tax','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    #can also change name of serializer object by giving source
    price = serializers.DecimalField(max_digits=6, decimal_places=2,source = 'unit_price')
    #can also add new field which is not in db
    tax = serializers.SerializerMethodField(method_name="calculate_tax")
    #to add relationship between different model
    collection = CollectionSerializer()
    #serializers.StringRelatedField()

    def calculate_tax(self,product:Product):
        return product.unit_price*Decimal(1.1)
    
    def create(self, validated_data):
        # Extract the collection data from the validated data
        collection_data = validated_data.pop('collection')

        # Create or get the collection instance
        collection, created = Collection.objects.get_or_create(**collection_data)

        # Now create the product with the remaining validated data and the collection instance
        product = Product.objects.create(collection=collection, **validated_data)
        
        return product
    

class ReviewSerializer(serializers.Serializer):
     class Meta:
          model = Review
          fields = ['id','product','description','name']