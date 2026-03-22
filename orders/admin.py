from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
  model = OrderItem
  extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
  list_filter = ('status', 'created_at')
  search_fields = ('user__username', 'stripe_session_id')
  ordering = ('-created_at',)
  inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ('product_name', 'price', 'quantity', 'order')
  search_fields = ('product_name',)