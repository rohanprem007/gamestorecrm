from django.urls import path
from . import views

urlpatterns = [
    # The empty string '' now points to the Home Page
    path('', views.home, name='home'),
    
    # The Dashboard is moved to /dashboard/
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Other functional modules
    path('inventory/', views.inventory_list, name='inventory'),
    path('customers/', views.customer_list, name='customers'),
    
    # Action logic
    path('sell/<int:product_id>/', views.process_sale, name='process_sale'),
]