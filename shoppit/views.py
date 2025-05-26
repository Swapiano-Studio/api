from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Product, Cart, CartItem, Transaction
from .serializers import (
    ProductsSerializer,
    DetailedProductSerializer,
    CartSerializer,
    SimpleCartSerializer,
    CartItemSerializer,
    UserSerializer,
)

BASE_URL = settings.REACT_BASE_URL

@api_view(["GET"])
def products(request):
    """
    Retrieve all available products.
    """
    queryset = Product.objects.all()
    serializer = ProductsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    """
    Retrieve detailed product information by slug.
    """
    product = get_object_or_404(Product, slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)


@api_view(["POST"])
def add_items(request):
    """
    Add a product to the cart or update the quantity if it already exists.
    Required: cart_code, product_id, quantity
    """
    try:
        cart_code = request.data["cart_code"]
        product_id = request.data["product_id"]
        quantity = int(request.data["quantity"])

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(cart_code=cart_code)
        product = get_object_or_404(Product, id=product_id)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity = quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({
            "data": serializer.data,
            "message": "Cart item added successfully" if created else "Cart item updated successfully"
        }, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response({"error": f"Missing field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def delete_items(request):
    """
    Delete a specific product from the cart.
    Required: cart_code, product_id (as query parameters)
    """
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")

    if not cart_code or not product_id:
        return Response({"error": "cart_code and product_id are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = get_object_or_404(Cart, cart_code=cart_code)
        product = get_object_or_404(Product, id=product_id)

        cartitem = CartItem.objects.get(cart=cart, product=product)
        cartitem.delete()

        return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def product_in_cart(request):
    """
    Check if a product exists in a cart.
    Required: cart_code, product_id (as query parameters)
    """
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")

    if not cart_code or not product_id:
        return Response({"error": "cart_code and product_id are required query parameters."},
                        status=status.HTTP_400_BAD_REQUEST)

    cart = get_object_or_404(Cart, cart_code=cart_code)
    product = get_object_or_404(Product, id=product_id)

    exists = CartItem.objects.filter(cart=cart, product=product).exists()
    return Response({"product_in_cart": exists})


@api_view(["GET"])
def get_cart_stat(request):
    """
    Retrieve summary of a paid cart.
    Required: cart_code (as query parameter)
    """
    cart_code = request.query_params.get("cart_code")

    if not cart_code:
        return Response({"error": "cart_code is required."}, status=status.HTTP_400_BAD_REQUEST)

    cart = get_object_or_404(Cart, cart_code=cart_code, paid=True)
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)


@api_view(["GET"])
def get_cart(request):
    """
    Retrieve detailed cart data.
    Required: cart_code (as query parameter)
    """
    cart_code = request.query_params.get("cart_code")

    if not cart_code:
        return Response({"error": "cart_code is required."}, status=status.HTTP_400_BAD_REQUEST)

    cart = get_object_or_404(Cart, cart_code=cart_code, paid=True)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_quantity(request):
    """
    Update the quantity of an existing cart item.
    Required: item_id, quantity
    """
    try:
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity"))

        if quantity <= 0:
            return Response({"error": "Quantity must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

        cartitem = get_object_or_404(CartItem, id=item_id)
        cartitem.quantity = quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "Cart item updated successfully."}, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
