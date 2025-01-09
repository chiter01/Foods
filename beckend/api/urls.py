from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, CategoryViewSet, CartViewSet, CartItemViewSet
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('foods', FoodViewSet, basename='food')
router.register('categories', CategoryViewSet, basename='category')
router.register('carts', CartViewSet, basename='cart')
router.register('cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls)),
]

urlpatterns += url_doc
