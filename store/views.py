from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product,Collection,Review,Cart,CartItem,Order
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer
from django.db.models import Count


#use of viewset

class ProductViewSet(ModelViewSet):
    # queryset =  Product.objects.select_related('collection').all()
    queryset = Product.objects.all()
    serializer_class= ProductSerializer 
    lookup_field= 'id'
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id']
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    # pagination_class= PageNumberPagination


#removing this cause we are using 3rd party library django_filters
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)

    #     return queryset


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count = Count('product')).all()
    serializer_class = CollectionSerializer
    lookup_field='id'

class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #in order to filter we r using get_queryset function instead of  queryset variable
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}


# class ProductList(ListCreateAPIView):
#     queryset =  Product.objects.select_related('collection').all()
#     serializer_class= ProductSerializer   

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class= ProductSerializer
#     lookup_field= 'id'
#     # def get(self,request,id):
#     #     product = get_object_or_404(Product, id=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count = Count('product')).all()
    serializer_class = CollectionSerializer


# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method=='GET':
#         queryset = Collection.objects.annotate(product_count = Count('product')).all()
#         serializer = CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer = CollectionSerializer(data= request.data)  
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)    




class CollectionView(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.annotate(
        product_count = Count('product'))
    serializer_class=CollectionSerializer
    lookup_field='id'

# @api_view(['GET','POST','PUT','DELETE'])
# def collection_view(request,id):
#     collection = get_object_or_404(Collection.objects.annotate(
#         product_count = Count('product')),id=id)

#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
    
#     elif request.method =='POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method =='PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


    
    # elif request.method =='DELETE':
    #     if collection.product.count()>0:
    #         return Response({'error':'Collection cannot be deleted'})
    #     collection.delete()
    #     return Response()


class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericViewSet):
        queryset= Cart.objects.prefetch_related('items__product').all()
        serializer_class= CartSerializer
        # lookup_field='id'

class CartItemViewSet(ModelViewSet):
     http_method_names=['get','post','patch','delete']
     def get_queryset(self):
          return CartItem.objects \
                .filter(card_id=self.kwargs['cart_pk']) \
                .select_related('product')
     
     def get_serializer_class(self):
          
          if self.request.method=='POST':
               return AddCartItemSerializer
          
          elif self.request.method=='PATCH':
               return UpdateCartItemSerializer
          return CartItemSerializer

     def get_serializer_context(self):
          return {'cart_id':self.kwargs['cart_pk']}
     

class OrderViewSet(ModelViewSet):
    queryset= Order.objects.all()
    serializer_class=OrderSerializer
    #  permission_classes=[IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def get_queryset(self):
         user = self.request.user

         if user.is_staff:
              