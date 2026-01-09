from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, Customer, Sale, DigitalKey

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(DigitalKey)
