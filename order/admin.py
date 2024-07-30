from django.contrib import admin
from .models import *

@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'buying_quantity',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'modified_at',)
