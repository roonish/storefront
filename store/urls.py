from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views

router = SimpleRouter()
router.register('product',views.ProductViewSet)
router.register('collection',views.CollectionViewSet)


urlpatterns = [
#router.urls

    path('',include(router.urls)),
    # path('product/',views.ProductList.as_view()),
    # #int will validate so only integer can be sent as an id
    # path('product_detail/<int:id>/',views.ProductDetail.as_view()),
    # path('collection/',views.CollectionList.as_view()),
    # path('collection/<int:id>/',views.CollectionView.as_view())

]