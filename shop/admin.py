from django.contrib import admin
from .models import Product, ProductImage, Cart, Tag


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Tag)
