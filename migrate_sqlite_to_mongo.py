import os
import django
from mongoengine import connect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from shoppit.mongo_models import ProductDoc, CartDoc, CartItemDoc, TransactionDoc
from core.mongo_models import CustomUserDoc
from shoppit.models import Product, Cart, CartItem, Transaction
from core.models import CustomUser
from django.conf import settings

# Koneksi ke MongoDB
connect(
    db=settings.MONGO_DB_NAME,
    host=settings.MONGO_URI,
    alias='default'
)

# Migrasi Product
for p in Product.objects.all():
    ProductDoc(
        name=p.name,
        slug=p.slug,
        image=str(p.image),
        description=p.description,
        price=p.price,
        category=p.category
    ).save()
print("Migrasi Product selesai.")

# Migrasi Cart
for c in Cart.objects.all():
    CartDoc(
        cart_code=c.cart_code,
        user_id=str(c.user.id) if c.user else "",
        paid=c.paid,
        created_at=c.created_at,
        modified_at=c.modified_at
    ).save()
print("Migrasi Cart selesai.")

# Migrasi CartItem
for ci in CartItem.objects.all():
    cart_doc = CartDoc.objects(cart_code=ci.cart.cart_code).first()
    product_doc = ProductDoc.objects(slug=ci.product.slug).first()
    if cart_doc and product_doc:
        CartItemDoc(
            cart=cart_doc,
            product=product_doc,
            quantity=ci.quantity
        ).save()
print("Migrasi CartItem selesai.")

# Migrasi Transaction
for t in Transaction.objects.all():
    cart_doc = CartDoc.objects(cart_code=t.cart.cart_code).first()
    TransactionDoc(
        ref=t.ref,
        cart=cart_doc,
        amount=t.amount,
        currency=t.currency,
        status=t.status,
        user_id=str(t.user.id) if t.user else "",
        created_at=t.created_at,
        modified_at=t.modified_at
    ).save()
print("Migrasi Transaction selesai.")

# Migrasi User
for u in CustomUser.objects.all():
    if not CustomUserDoc.objects(username=u.username).first():
        CustomUserDoc(
            username=u.username,
            email=u.email,
            first_name=u.first_name,
            last_name=u.last_name,
            city=u.city,
            state=u.state,
            address=u.address,
            phone_number=u.phone_number,
            password=u.password,  # Sudah di-hash
            is_active=u.is_active,
            is_staff=u.is_staff,
            is_superuser=u.is_superuser,
            date_joined=u.date_joined
        ).save()
print("Migrasi User selesai.")