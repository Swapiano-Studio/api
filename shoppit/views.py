from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import (
    ProductsSerializer,
    DetailedProductSerializer,
    CartSerializer,
    SimpleCartSerializer,
    CartItemSerializer,
    UserSerializer,
)
from .models import Product, Cart, CartItem  # Ganti ke model Django ORM

BASE_URL = settings.REACT_BASE_URL

@api_view(["GET"])
def products(request):
    """
    Retrieve all available products.
    """
    queryset = Product.objects.all()
    serializer = ProductsSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    """
    Retrieve detailed product information by slug.
    """
    product = Product.objects.filter(slug=slug).first()
    if not product:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = DetailedProductSerializer(product, context={"request": request})
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

        cart = Cart.objects.filter(cart_code=cart_code).first()
        if not cart:
            cart = Cart(cart_code=cart_code)
            cart.save()

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cartitem = CartItem.objects.filter(cart=cart, product=product).first()
        created = False
        if not cartitem:
            cartitem = CartItem(cart=cart, product=product, quantity=quantity)
            created = True
        else:
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
        cart = Cart.objects.filter(cart_code=cart_code).first()
        product = Product.objects.filter(id=product_id).first()
        if not cart or not product:
            return Response({"error": "Cart or Product not found."}, status=status.HTTP_404_NOT_FOUND)
        cartitem = CartItem.objects.filter(cart=cart, product=product).first()
        if not cartitem:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        cartitem.delete()

        return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_200_OK)
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
        return Response({"error": "cart_code and product_id are required query parameters."}, status=status.HTTP_400_BAD_REQUEST)

    cart = Cart.objects.filter(cart_code=cart_code).first()
    product = Product.objects.filter(id=product_id).first()

    exists = False
    if cart and product:
        exists = CartItem.objects.filter(cart=cart, product=product).first() is not None
    return Response({"product_in_cart": exists})


@api_view(["GET"])
def get_cart_stat(request):
    """
    Retrieve summary of a cart (paid or unpaid).
    Required: cart_code (as query parameter)
    """
    cart_code = request.query_params.get("cart_code")

    if not cart_code:
        return Response({"error": "cart_code is required."}, status=status.HTTP_400_BAD_REQUEST)

    cart = Cart.objects.filter(cart_code=cart_code).first()  # Hilangkan paid=True agar cart apapun bisa diambil
    if not cart:
        return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    items = CartItem.objects.filter(cart=cart)
    cart.items.set(items)  # Use set() instead of direct assignment
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

    cart = Cart.objects.filter(cart_code=cart_code).first()  # Hapus paid=True agar cart yang belum dibayar bisa ditemukan
    if not cart:
        return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    items = CartItem.objects.filter(cart=cart)
    cart.items.set(items)  # Use set() instead of direct assignment
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

        cartitem = CartItem.objects.filter(id=item_id).first()
        if not cartitem:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
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
