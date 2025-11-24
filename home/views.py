from django.shortcuts import render
from shop.models import Product, Review

def home(request):
    # Top price 6 products
    top_products = Product.objects.order_by('-price')[:6]

    # Latest 3 reviews across all products
    latest_reviews = Review.objects.order_by('-created_at')[:3]

    # Fetch all categories
    from shop.models import Category
    categories = Category.objects.all()

    return render(request, 'home/home.html', {
        "top_products": top_products,
        "latest_reviews": latest_reviews,
        "categories": categories,
    })
