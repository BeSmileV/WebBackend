from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductListView, ProductDetailView, CartView

router = DefaultRouter()
router.register(r'cart', CartView, basename='cart')

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
] + router.urls
