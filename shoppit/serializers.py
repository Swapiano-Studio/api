from rest_framework import serializers
from .mongo_models import ProductDoc, CartDoc, CartItemDoc
from django.contrib.auth import get_user_model
from django.conf import settings

class ProductsSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    image = serializers.SerializerMethodField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    price = serializers.FloatField()
    category = serializers.CharField(allow_blank=True, allow_null=True)

    def get_image(self, obj):
        request = self.context.get('request')
        # Clean up image path: remove any leading 'img/', '/img/', or 'img\\'
        image_path = obj.image or ''
        image_path = image_path.replace('\\', '/').lstrip('/')
        if image_path.lower().startswith('img/'):
            image_path = image_path[4:]
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return settings.MEDIA_URL + image_path

class DetailedProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    slug = serializers.CharField()
    image = serializers.SerializerMethodField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    price = serializers.FloatField()
    similiar_products = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        # Clean up image path: remove any leading 'img/', '/img/', or 'img\\'
        image_path = obj.image or ''
        image_path = image_path.replace('\\', '/').lstrip('/')
        if image_path.lower().startswith('img/'):
            image_path = image_path[4:]
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return settings.MEDIA_URL + image_path

    def get_similiar_products(self, obj):
        products = ProductDoc.objects(category=obj.category, id__ne=obj.id)[:5]
        return ProductsSerializer(products, many=True, context=self.context).data

class CartItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    quantity = serializers.IntegerField()
    product = ProductsSerializer()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.quantity * float(obj.product.price)

class CartSerializer(serializers.Serializer):
    id = serializers.CharField()
    cart_code = serializers.CharField()
    items = CartItemSerializer(many=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    def get_sum_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items)

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items)

class SimpleCartSerializer(serializers.Serializer):
    id = serializers.CharField()
    cart_code = serializers.CharField()
    num_of_items = serializers.SerializerMethodField()

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "city", "state", "address", "phone_number"]