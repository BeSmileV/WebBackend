from django.conf import settings
from rest_framework import serializers

from .models import Product, Cart


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_images(self, obj):
        media_url = settings.MEDIA_URL
        return [media_url + image.image.name for image in obj.images.all()]


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'products']
