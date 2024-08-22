from django.contrib import admin
from .models import Workshop, Event

from services.admin import WorkshopImageInline

class WorkshopAdmin(admin.ModelAdmin):
    
    inlines = [WorkshopImageInline]
    
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'address', 'date')
        }),
        ('Details', {
            'fields': ('workshop_level', 'tags', 'organized_by', 'conducted_by_artisan', 'artisan', 'price'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('title', 'date', 'address', 'price', 'conducted_by_artisan', 'artisan', 'created_at')
    
    # Filter options in the admin list view
    list_filter = ('workshop_level', 'conducted_by_artisan', 'date', 'price')
    
    # Search fields for the admin search bar
    search_fields = ('title', 'description', 'organized_by', 'artisan__name')

    # Ordering options for the list view
    ordering = ('-date',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'modified_at')

class EventAdmin(admin.ModelAdmin):
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'address', 'date')
        }),
        ('Details', {
            'fields': ('tags',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('title', 'date', 'address', 'created_at')

    # Filter options in the admin list view
    list_filter = ('date',)
    
    # Search fields for the admin search bar
    search_fields = ('title', 'description', 'address')

    # Ordering options for the list view
    ordering = ('-date',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'modified_at')

# Register the models with their respective admin configurations
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Event, EventAdmin)
