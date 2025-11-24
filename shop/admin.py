from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem, Review
from django.urls import reverse
from django.utils.html import format_html
# Category & Product
admin.site.register(Category)
admin.site.register(Product)

# OrderItem Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')  # already আছে
    can_delete = False  # Optional: prevent deleting from admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_method', 'transaction_id', 'status', 'created_at', 'ordered_products')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('user__username', 'id', 'transaction_id')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    readonly_fields = ('shipping_address',)

    # Custom method to show products + quantity
    def ordered_products(self, obj):
        items = obj.orderitem_set.all()  # all OrderItem for this order
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in items])
    ordered_products.short_description = "Products"


admin.site.register(Order, OrderAdmin)

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')

admin.site.register(Review, ReviewAdmin)

class SalesReportAdminLink(admin.ModelAdmin):
    change_list_template = "admin/sales_report_link.html"

admin.site.index_template = "admin/custom_index.html"