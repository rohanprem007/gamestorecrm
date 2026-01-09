from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    PLATFORM_CHOICES = (
        ('pc', 'PC'),
        ('ps5', 'PlayStation 5'),
        ('xbox', 'Xbox Series X'),
        ('switch', 'Nintendo Switch'),
    )
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField(default=0)
    is_digital = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"

class Customer(models.Model):
    # Linking to Django's built-in User for login/auth
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gamer_tag = models.CharField(max_length=50, blank=True)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Sale: {self.product.title} to {self.customer}"

class DigitalKey(models.Model):
    # For digital games, store the activation key
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={'is_digital': True})
    key_code = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Key for {self.product.title}"