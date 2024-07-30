from django.contrib import admin
from .models import *

@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'buying_quantity', 'status', 'subtotal', 'total', 'created_at', 'modified_at')
    list_filter = ('status', 'created_at', 'modified_at')
    search_fields = ('order__id', 'product__title')
    readonly_fields = ('subtotal', 'total', 'created_at', 'modified_at')
    fieldsets = (
        (None, {
            'fields': ('order', 'product', 'buying_quantity', 'status', 'estimate_delivery_time')
        }),
        ('Costing', {
            'fields': ('subtotal', 'total'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_mode', 'created_at', 'modified_at',)
