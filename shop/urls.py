from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('sales-reports/', views.sales_report_view, name='sales_reports'),
    path("sales-report/export-excel/", views.export_sales_excel, name="export_sales_excel"),
]
