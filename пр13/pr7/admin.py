from django.contrib import admin
from pr7.models import Product, Category
from order.models import Order, OrderItem


# Register your models here.

@admin.register(Product, Category)
class AdminProduct(admin.ModelAdmin):
    pass

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_user', 'customer_email', 'order_date', 'status')
    search_fields = ('customer_user', 'customer_email', 'status')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemInline]
