"""Admin dashboard: manage orders, statuses and promo codes."""
from django.contrib import admin
from .models import Order, OrderItem, PromoCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'grand_total',
                    'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    list_editable = ('status',)          # update order status from the list
    search_fields = ('full_name', 'email', 'phone', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('subtotal', 'tax', 'delivery_charge',
                       'discount', 'grand_total', 'created_at')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'user', 'used', 'created_at')
    list_filter = ('used',)
    search_fields = ('code', 'user__username')
