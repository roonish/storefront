from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register('product',views.ProductViewSet, basename='products')
router.register('collection',views.CollectionViewSet)

products_router =  routers.NestedDefaultRouter(router, 'product', lookup = 'product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')


urlpatterns = [
#router.urls

    path('',include(router.urls)),
    path('',include(products_router.urls)),

    # path('product/',views.ProductList.as_view()),
    # #int will validate so only integer can be sent as an id
    # path('product_detail/<int:id>/',views.ProductDetail.as_view()),
    # path('collection/',views.CollectionList.as_view()),
    # path('collection/<int:id>/',views.CollectionView.as_view())

]