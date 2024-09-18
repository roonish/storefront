from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,Value,Func,F,ExpressionWrapper,DecimalField
from django.db.models.aggregates import Min
from django.db import transaction, connection
from store.models import Product,OrderItem,Collection,Order


def say_hello(request):
    #for all value
    # querySet = Product.objects.all()
    # for product in querySet:
    #     print(product.title)

    #for single value
    # unitPrice = Product.objects.get(id=5)
    # print(unitPrice.description)

    # #to filter
    # desc = Product.objects.filter(id=5).first()
    # print(desc.description)

    #using lookups
    # _ _ gt, lt,gte,lte etc
    # queryset = Product.objects.filter(unit_price__range=(20,50))

    #using q operators for OR AND 
    # inventory<10 and price>20
    # queryset = Product.objects.filter(inventory__lt=10,unit_price__gt=20)

    # inveotnroy>30 OR price<50
    # FOR NOT USE ~ SIGN. i.e. ~Q(.....)
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))

    #to sort by ascendening and desc
    # default ascending sort.
    # if want desc add - sign. eg: order_by('-title')
    # queryset = Product.objects.order_by('title')

    #to limit data
    # if i want to send only 5 first data
    # [5:10], start from 5 and do till 10
    # queryset = Product.objects.all()[:5]

    #values method to only get column that we want instead of showing all
    # difer function can be used to exclude that. eg:if defer(desc), all field except desc will be selected
    # queryset = Product.objects.values('unit_price')

    # in order to reload other field of other related table we use select_related
    # use select_related when other end relation has one instance. eg product have one collection . so for that use select_related
    # use prefetch_related when other end relatuon has multiple instance. eg  product have many promotion. sp tp load promotion use prefetch
    # queryset = Product.objects.select_related('collection').all()

# to use max, avg, like aggregate , use aggregate function. import django.db.models.aggregates import Count,Max,Min,Sum,Avg
    # queryset = Product.objects.aggregate(min_price= Min('unit_price'))

# in order to use boolean in value we can import value from db.model ,
# to add new attribute in table use annootate
    # queryset = Product.objects.annotate(new_field = Value(True))

    # calling db functions like concat,for that need to import func from django,db.model
    # queryset = Product.objects.annotate(unit_inventory = Func(F('unit_price'),F('inventory')
    # ,function='CONCAT'))

    # USE OF EXPRESSION WRAPPER,import expression wrapper from db.model
    # discounted_price =  ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price = discounted_price)

    #Caching queryset Insert into database
    # collection = Collection()
    # collection.title='New Collection'
    # collection.featured_product = Product(id=1)
    # collection.save()

    # or we can use simple cmd
    # Collection.objects.create(title='New Collection', featured_product = Product(id=1))

    # to update
    # have to call that data then update any value
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    # Or first have to filter whidch row to update then use update function
    # Collection.objects.filter(pk=11).update(featured_product=None)

    #to delete all data or more then 1 data
    Collection.objects.filter(pk__gt=5).delete()

    #or oldw way
    # collection = Collection(pk=5)
    # collection.delete()

    #transaction
    # sometime we want to do 2 or more task and it should either be success together or if anything fail all should be fsil
    # example is creating 2 row and if 1 row fails other may be saved which will be creating problem. so we have to not save both at that time
# for that import transaction from django.db and use with transaction.atomic()

    # with transaction.atomic():

    #     order = Order()
    #     order.customer_id=1
    #     order.save()

    #     orderItem = OrderItem()
    #     orderItem.order=order
    #     orderItem.unit_price=100
    #     orderItem.save()

    # To execute raw sql queries
    # Product.objects.raw('SELECT id,title FROM  store_product')
    # or
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT *')

    return render(request, 'hello.html', {'name': 'Mosh','queryset':list(queryset)})
