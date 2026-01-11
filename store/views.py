from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from .models import Product, Customer, Sale

def home(request):
    """
    Renders the high-energy landing page.
    """
    # We pass 'hide_sidebar': True to render the full-screen landing experience
    return render(request, 'store/home.html', {'hide_sidebar': True})

def dashboard(request):
    """
    The main Command Center view.
    """
    products = Product.objects.all()
    recent_sales = Sale.objects.order_by('-sale_date')[:5]
    
    # Calculate Total Revenue
    total_revenue = Sale.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Stats Counts
    sales_count = Sale.objects.count()
    customers_count = Customer.objects.count()
    
    # Logic for Leaderboard (Top Customers by XP)
    top_customers = Customer.objects.order_by('-loyalty_points')[:5]

    context = {
        'products': products,
        'recent_sales': recent_sales,
        'total_revenue': total_revenue,
        'sales_count': sales_count,
        'customers_count': customers_count,
        'top_customers': top_customers,
    }
    return render(request, 'store/dashboard.html', context)

def inventory_list(request):
    products = Product.objects.all()
    return render(request, 'store/inventory.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    # Assuming you have a template for customers, otherwise pointing to a placeholder
    return render(request, 'store/customers.html', {'customers': customers})

def process_sale(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # For demo, if user is superuser or logged in, use them. 
    # If not, use/create a default 'Guest' or 'StoreAdmin' customer profile.
    if hasattr(request.user, 'customer'):
        customer = request.user.customer
    else:
        # Fallback for testing if admin doesn't have a linked customer profile
        customer, created = Customer.objects.get_or_create(
            phone="000-000-0000",
            defaults={'user': request.user, 'gamer_tag': 'AdminUser'}
        )

    if product.stock_count > 0:
        try:
            with transaction.atomic():
                Sale.objects.create(
                    customer=customer,
                    product=product,
                    amount_paid=product.price
                )
                product.stock_count -= 1
                product.save()
                
                # Award XP (1 point per dollar)
                points = int(product.price)
                customer.loyalty_points += points
                customer.save()

                messages.success(request, f"SOLD: {product.title}! +{points} XP to {customer.gamer_tag}")
        except Exception as e:
            messages.error(request, "Transaction Failed. System Rolled Back.")
    else:
        messages.error(request, f"OUT OF STOCK: {product.title}")

    return redirect('dashboard')