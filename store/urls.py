from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('customers/', views.customer_list, name='customers'),
    path('sales/', views.sales_list, name='sales'),
    path('sell/<int:product_id>/', views.process_sale, name='process_sale'),
]
