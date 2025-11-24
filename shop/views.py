import openpyxl
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Product, Order, OrderItem, Category
from django.contrib import messages
from .models import  Review
from .forms import ReviewForm
from django.db.models import Avg, Count, Sum
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncDate
from datetime import datetime
from django.utils import timezone





def product_list(request):
    products = Product.objects.all()
    
    # Category filter by ID
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search by category name OR product name
    query = request.GET.get('q')
    if query:
        # Try to find category by name
        category = Category.objects.filter(name__icontains=query).first()
        if category:
            products = products.filter(category=category)
        else:
            # fallback: search by product name
            products = products.filter(name__icontains=query)
    
    # Pagination (6 products per page)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'shop/product_list.html', {
        'products': page_obj,
        'categories': categories
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Calculate average rating and total number of reviews
    avg_rating_float = reviews.aggregate(average=Avg('rating'))['average'] or 0
    total_reviews = reviews.aggregate(count=Count('id'))['count'] or 0

    # Round average rating to nearest integer
    avg_rating = int(round(avg_rating_float))

    if request.user.is_authenticated and request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews
    })


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def update_cart(request, id):
    cart_item = CartItem.objects.get(id=id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.total_price for item in cart_items])
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        shipping_address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')  # may be None

        # ===============================
        # Stock Verification
        # ===============================
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request, 
                    f"Cannot place order for {item.product.name}. Available stock: {item.product.stock}"
                )
                return redirect('cart_view')  # back to cart

        # ===============================
        # Create Order
        # ===============================
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            shipping_address=shipping_address,
            status="Pending",
            payment_method=payment_method,
            transaction_id=transaction_id if payment_method == 'send_money' else None
        )

        # ===============================
        # Add Order Items & Reduce Stock
        # ===============================
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()

        # ===============================
        # Clear Cart
        # ===============================
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate total spent for completed orders only
    total_spent = orders.filter(status__in=['Shipped', 'Delivered']).aggregate(
        total= Sum('total_price')
    )['total'] or 0

    return render(request, 'shop/order_history.html', {
        'orders': orders,
        'total_spent': total_spent
    })


def category_products(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'products': products
    })



@staff_member_required
def sales_report_view(request):

    # Dropdown values
    months = list(range(1, 13))
    years = [datetime.now().year - i for i in range(6)]

    # User filter values
    month = request.GET.get("month")
    year = request.GET.get("year")

    # Delivered orders only
    orders = Order.objects.filter(status='Delivered')

    # Apply filtering
    if month:
        orders = orders.filter(created_at__month=month)
    if year:
        orders = orders.filter(created_at__year=year)

    # Group by date
    delivered_orders = (
        orders.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total_sales=Sum('total_price'))
        .order_by('-date')
    )

    # Total sales of filtered dates
    total_sales = orders.aggregate(sum=Sum('total_price'))["sum"] or 0

    return render(request, 'admin/sales_report.html', {
        'report': delivered_orders,
        'months': months,
        'years': years,
        'month': month,
        'year': year,
        'total_sales': total_sales,
        'now': timezone.now(),
        'currency_symbol': "$",
    })

@staff_member_required
def export_sales_excel(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    orders = Order.objects.filter(status='Delivered')

    if month:
        orders = orders.filter(created_at__month=month)
    if year:
        orders = orders.filter(created_at__year=year)

    # Group by date
    report = (
        orders.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total_sales=Sum('total_price'))
        .order_by('-date')
    )

    # Convert to DataFrame
    df = pd.DataFrame(report)
    df = df.rename(columns={'date': 'Date', 'total_sales': 'Total Sales'})

    # Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    df.to_excel(response, index=False)

    return response