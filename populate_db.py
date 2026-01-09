import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Category, Product, Customer
from django.contrib.auth.models import User

def populate():
    # 1. Create Categories
    action, _ = Category.objects.get_or_create(name="Action")
    rpg, _ = Category.objects.get_or_create(name="RPG")
    hardware, _ = Category.objects.get_or_create(name="Hardware")

    # 2. Create Products
    games = [
        {"title": "Elden Ring", "cat": rpg, "plat": "pc", "price": 59.99, "stock": 10},
        {"title": "Spider-Man 2", "cat": action, "cat": action, "plat": "ps5", "price": 69.99, "stock": 5},
        {"title": "DualSense Controller", "cat": hardware, "plat": "ps5", "price": 74.99, "stock": 15},
    ]

    for game in games:
        Product.objects.get_or_create(
            title=game['title'],
            category=game['cat'],
            platform=game['plat'],
            price=game['price'],
            stock_count=game['stock']
        )

    # 3. Create a Test Customer
    user, created = User.objects.get_or_create(username="test_gamer")
    if created:
        user.set_password("password123")
        user.save()
    
    Customer.objects.get_or_create(
        user=user,
        phone="1234567890",
        gamer_tag="ProGamer99",
        loyalty_points=100
    )

    print("Successfully added test data!")

if __name__ == '__main__':
    populate()