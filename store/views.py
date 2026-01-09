from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Product, Customer, Sale


from django.shortcuts import render
from .models import Product, Customer, Sale

# 1. Dashboard (Already created, but ensure it's here)
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'store/dashboard.html', {'products': products})

# 2. Inventory Page
def inventory_list(request):
    products = Product.objects.all()
    return render(request, 'store/inventory.html', {'products': products})

# 3. Customers Page
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'store/customers.html', {'customers': customers})

# 4. Sales History Page
def sales_list(request):
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'store/sales.html', {'sales': sales})



def process_sale(request, product_id):
    # Fetch the product being sold
    product = get_object_or_404(Product, id=product_id)
    
    # Fetch the customer (assuming the logged-in user is the customer for this demo)
    # In a staff-facing CRM, you'd select a customer ID from a form instead.
    customer = get_object_or_404(Customer, user=request.user)

    # Validation: Is there stock?
    if product.stock_count > 0:
        try:
            # Atomic block ensures all 3 updates succeed or all 3 fail
            with transaction.atomic():
                # Step 1: Create the Sale Record
                Sale.objects.create(
                    customer=customer,
                    product=product,
                    amount_paid=product.price
                )

                # Step 2: Decrease Stock
                product.stock_count -= 1
                product.save()

                # Step 3: Add Loyalty Points (e.g., 1 point per $1 spent)
                points_earned = int(product.price)
                customer.loyalty_points += points_earned
                customer.save()

                messages.success(request, f"Sale Completed! {product.title} sold to {customer.gamer_tag}. {points_earned} XP awarded!")
        
        except Exception as e:
            messages.error(request, "Transaction failed. Database has been rolled back.")
    else:
        messages.error(request, f"Error: {product.title} is currently out of stock.")

    return redirect('dashboard')