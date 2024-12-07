import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer


class ProductFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['tag']


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return Response({'message': f'Product {product.name} added to cart'})

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        if product in cart.products.all():
            cart.products.remove(product)
            return Response({'message': f'Product {product.name} removed from cart'})

        return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def buy(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.products.exists():
            return Response({'message': 'Cart is empty. Add products to buy.'}, status=status.HTTP_400_BAD_REQUEST)

        cart.products.clear()
        return Response({'message': 'Purchase successful! Your cart is now empty.'})
