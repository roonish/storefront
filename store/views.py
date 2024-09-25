from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
from django.db.models import Count

# Create your views here.
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':  
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)



@api_view(['GET','POST'])
def collection_list(request):
    if request.method=='GET':
        queryset = Collection.objects.annotate(product_count = Count('product')).all()
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = CollectionSerializer(data= request.data)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    


@api_view(['GET','POST','PUT','DELETE'])
def collection_view(request,id):
    collection = get_object_or_404(Collection.objects.annotate(
        product_count = Count('product')),id=id)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method =='POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method =='PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    
    elif request.method =='DELETE':
        if collection.product.count()>0:
            return Response({'error':'Collection cannot be deleted'})
        collection.delete()
        return Response()


