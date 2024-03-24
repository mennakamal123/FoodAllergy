from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, CartViewSet,OrderViewSet, AllergyProductViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('allergy-products/<int:pk>/allergy_products/', AllergyProductViewSet.as_view({'get': 'allergy_products'}), name='allergy-products')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)