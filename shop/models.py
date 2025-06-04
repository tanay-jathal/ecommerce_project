from django.db import models
from django.contrib.auth.models import User

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    raw_password = models.CharField(max_length=128)  # Not secure! Demo only
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username if self.user else 'No User'

class Category(models.Model):  # Capitalized 'Category' for proper class naming
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' → '.join(reversed(full_path))

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter Price in INR")
    image = models.ImageField(upload_to='products_/')
    stock = models.PositiveIntegerField(default=0, help_text="Number of items available in stock")
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())
    total_price.short_description = 'Total Price'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products_/')
    stock = models.PositiveIntegerField(default=0, help_text="Number of items available in stock")
    in_stock = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Wishlist item for {self.user.username} - {self.product.name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
