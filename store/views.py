from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
from django.db.models import Count


#use of viewset

class ProductViewSet(ModelViewSet):
    queryset =  Product.objects.select_related('collection').all()
    serializer_class= ProductSerializer 
    lookup_field= 'id'


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count = Count('product')).all()
    serializer_class = CollectionSerializer
    lookup_field='id'




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


