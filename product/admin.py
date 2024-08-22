from django.contrib import admin
from .models import *

from services.admin import ProductImageInline

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    inlines = [ProductImageInline]
    
    # Define fieldsets for the admin form layout
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'back_story', 'price', 'is_customizable',)
        }),
        ('Details', {
            'fields': ('dimensions', 'product_details', 'raw_material', 'category', 'quantity', 'restock_date'),
            'classes': ('collapse',),  # Optional: collapsible section
        }),
        ('Status', {
            'fields': ('is_verified', 'created_at', 'modified_at', 'cancelled_at'),
            'classes': ('collapse',),  # Optional: collapsible section
        }),
        ('Artisan Info', {
            'fields': ('artisan',),
        }),
    )
    
    # Define list display fields
    list_display = (
        'id',
        'title',
        'artisan',
        'price',
        'category',
        'quantity',
        'is_verified',
        'created_at',
        'modified_at'
    )
    
    # Define list filter options
    list_filter = (
        'category',
        'is_verified',
        'raw_material',
        'created_at',
        'modified_at',
    )
    
    # Add search functionality
    search_fields = (
        'title',
        'description',
        'back_story',
        'artisan__name',  # Assumes Artisan model has a 'name' field
    )
    
    # Define ordering of list display
    ordering = ('-created_at',)
    
    # Define readonly fields (if any)
    readonly_fields = ('created_at', 'modified_at', 'cancelled_at')
