from rest_framework import serializers
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
        image_field = obj.image
        image_path = ''
        if image_field:
            if hasattr(image_field, 'url'):
                image_path = image_field.url
            else:
                image_path = str(image_field)
            image_path = image_path.replace('\\', '/').lstrip('/')
            if image_path.lower().startswith('img/'):
                image_path = image_path[4:]
        final_path = settings.MEDIA_URL + image_path if image_path else ''
        final_path = final_path.replace('/img/img/', '/img/')
        if request:
            return request.build_absolute_uri(final_path)
        return final_path

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
        image_field = obj.image
        image_path = ''
        if image_field:
            if hasattr(image_field, 'url'):
                image_path = image_field.url
            else:
                image_path = str(image_field)
            image_path = image_path.replace('\\', '/').lstrip('/')
            # Remove leading 'img/' if present
            if image_path.lower().startswith('img/'):
                image_path = image_path[4:]
        # Avoid double 'img/img/'
        final_path = settings.MEDIA_URL + image_path if image_path else ''
        final_path = final_path.replace('/img/img/', '/img/')
        if request:
            return request.build_absolute_uri(final_path)
        return final_path

    def get_similiar_products(self, obj):
        # Find up to 5 other products in the same category, excluding the current product
        if not obj.category:
            return []
        from .models import Product
        similiar = Product.objects.filter(category=obj.category).exclude(id=obj.id)
        return ProductsSerializer(similiar, many=True, context=self.context).data

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
        # obj.items is a RelatedManager, use .all() to iterate
        return sum(item.product.price * item.quantity for item in obj.items.all())

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

class SimpleCartSerializer(serializers.Serializer):
    id = serializers.CharField()
    cart_code = serializers.CharField()
    num_of_items = serializers.SerializerMethodField()

    def get_num_of_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "city", "state", "address", "phone_number"]