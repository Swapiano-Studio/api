import locale
from rest_framework import serializers
from .models import Product, Cart, CartItem
from django.contrib.auth import get_user_model

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'price', 'category']


class DetailedProductSerializer(serializers.ModelSerializer):
    similiar_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'price', 'similiar_products']

    def get_similiar_products(self, obj):
        products = Product.objects.filter(category=obj.category).exclude(id=obj.id)[:5]
        return ProductsSerializer(products, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total']

    def get_total(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'items', 'sum_total', 'num_of_items', 'created_at', 'modified_at']

    def get_sum_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    

class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'num_of_items']

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "city", "state", "address", "phone_number"]