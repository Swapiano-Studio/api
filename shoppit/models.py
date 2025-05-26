from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('SP', 'Supplement'),
        ('SC', 'Self Care'),
        ('HB', 'Health and Beauty'),
        ('ETC', 'Others'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="img")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate slug if not set
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)


class Cart(models.Model):
    cart_code = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.cart_code} - {'Paid' if self.paid else 'Unpaid'}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart {self.cart.cart_code})"

    class Meta:
        unique_together = ('cart', 'product')  

class Transaction(models.Model):
    ref = models.CharField(max_length=255, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="NGN")
    status = models.CharField(max_length=20, default="pending")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Transactin {self.ref} - {self.status}"