from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem,Order,OrderItem
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
    

class ReviewSerializer(serializers.ModelSerializer):
     class Meta:
          model = Review
          fields = ['id','description','name']

     def create(self, validated_data):
        # Get the product instance
        product_id = self.context['product_id']
        
        review = Review.objects.create(product_id=product_id, **validated_data)
        return review

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['id','title','unit_price']

     
class CartItemSerializer(serializers.ModelSerializer):
     product = SimpleProductSerializer()
     total_price = serializers.SerializerMethodField()

     def get_total_price (self, cart_item:CartItem):
          return cart_item.quantity* cart_item.product.unit_price
     
     class Meta:
          model = CartItem
          fields = ['id','product','quantity','total_price' ] 
     
class CartSerializer(serializers.ModelSerializer):
     id = serializers.UUIDField(read_only = True)
     items = CartItemSerializer(many=True,read_only=True)
     total_price = serializers.SerializerMethodField()

     def get_total_price(self,cart):
       return sum( [item.quantity* item.product.unit_price for item in cart.items.all()])  
     
     class Meta:
          model = Cart
          fields = ['id','created_at','items','total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given id was found')
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quanity']
        cart_id = self.context['cart_id']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity +=quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance=  CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance 

    class Meta:
        model = CartItem
        fiekds = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields = ['id','product','unit_price','quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','customer','payment_status','placed_at','items']