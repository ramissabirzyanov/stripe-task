from django.contrib import admin

from payment_app.order.models import Order


@admin.register(Order)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_items', 'total_price']
