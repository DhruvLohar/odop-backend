from django.contrib import admin
from .models import Artisan

from django.utils.html import format_html

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        # Get the original queryset and include inactive users
        qs = super().get_queryset(request)
        return qs
    
    readonly_fields = ('id', 'access_token', 'created_at', 'modified_at',)
    
    fieldsets = (
        (None, {'fields': ('id', 'is_active', 'verified_by_authority', 'valid_otp',)}),
        ('Personal Information', {
            'fields': ('profile_image', 'name', 'phone_number', 'email', 'gender', 'age',)
        }),
        ('Address', {
            'fields': ('address', 'district', 'state', 'postal_code',)
        }),
        ('Documents', {
            'fields': (
                'aadhar_number', 'aadhar_image', 
                'pan_number', 'pan_image',
            )
        }),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'modified_at',)}),
        ('User Tokens', {'fields': ('access_token', 'fcm_token',)}),
    )
    
    def copy_access_token(self, obj):
        return format_html(
            '<button onclick="navigator.clipboard.writeText(\'{0}\').then(() => alert(\'Access Token copied to clipboard\'))">Copy</button>',
            obj.access_token
        )
        
    list_display = ['id', 'name', 'phone_number', 'copy_access_token']
    
