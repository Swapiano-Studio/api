from mongoengine import Document, StringField, DecimalField, ReferenceField, BooleanField, DateTimeField, IntField, CASCADE
from datetime import datetime

class ProductDoc(Document):
    name = StringField(required=True)
    slug = StringField()
    image = StringField()
    description = StringField()
    price = DecimalField()
    category = StringField()
    meta = {'collection': 'product'}

class CartDoc(Document):
    cart_code = StringField(required=True, unique=True)
    user_id = StringField()  # Simpan id user sebagai string
    paid = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'cart'}

class CartItemDoc(Document):
    cart = ReferenceField(CartDoc, reverse_delete_rule=CASCADE)
    product = ReferenceField(ProductDoc, reverse_delete_rule=CASCADE)
    quantity = IntField(default=1)
    meta = {'collection': 'cartitem'}

class TransactionDoc(Document):
    ref = StringField(required=True, unique=True)
    cart = ReferenceField(CartDoc, reverse_delete_rule=CASCADE)
    amount = DecimalField()
    currency = StringField(default="NGN")
    status = StringField(default="pending")
    user_id = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'transaction'}