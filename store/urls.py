from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.product_list),
    #int will validate so only integer can br sent as an id
    path('product_detail/<int:id>/',views.product_detail),
    path('collection/',views.collection_list),
    path('collection/<int:id>/',views.collection_view)

]