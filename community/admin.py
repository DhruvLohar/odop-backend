from django.contrib import admin
from .models import *

class JobPostAdmin(admin.ModelAdmin):
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('artisan', 'title', 'description', 'vacancy', 'prerequisites')
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('id', 'title', 'artisan', 'vacancy', 'is_active', 'created_at')
    
    # Filter options in the admin list view
    list_filter = ('is_active', 'artisan')
    
    # Search fields for the admin search bar
    search_fields = ('title', 'description', 'artisan__name')
    
    # Ordering options for the list view
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at', 'modified_at')

class JobPostApplicationRequestAdmin(admin.ModelAdmin):
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('artisan', 'job_post', 'about')
        }),
        ('Status', {
            'fields': ('status',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('id', 'artisan', 'job_post', 'status', 'created_at')
    
    # Filter options in the admin list view
    list_filter = ('status', 'job_post')
    
    # Search fields for the admin search bar
    search_fields = ('artisan__name', 'job_post__title', 'about')
    
    # Ordering options for the list view
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at',)

class RentalMachineAdmin(admin.ModelAdmin):
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('artisan', 'title', 'description', 'starting_time', 'ending_time')
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('id', 'title', 'artisan', 'starting_time', 'ending_time', 'is_active', 'created_at')
    
    # Filter options in the admin list view
    list_filter = ('is_active', 'artisan')
    
    # Search fields for the admin search bar
    search_fields = ('title', 'description', 'artisan__name')
    
    # Ordering options for the list view
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at', 'modified_at')

class RentalMachineBookingRequestAdmin(admin.ModelAdmin):
    # Fieldsets to group fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('artisan', 'rental_machine', 'start_time', 'end_time', 'purpose')
        }),
        ('Status', {
            'fields': ('status',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # List display fields in the admin list view
    list_display = ('id', 'artisan', 'rental_machine', 'start_time', 'end_time', 'status', 'created_at')
    
    # Filter options in the admin list view
    list_filter = ('status', 'rental_machine')
    
    # Search fields for the admin search bar
    search_fields = ('artisan__name', 'rental_machine__title', 'purpose')
    
    # Ordering options for the list view
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at',)

# Register the models with their respective admin configurations
admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobPostApplicationRequest, JobPostApplicationRequestAdmin)
admin.site.register(RentalMachine, RentalMachineAdmin)
admin.site.register(RentalMachineBookingRequest, RentalMachineBookingRequestAdmin)
