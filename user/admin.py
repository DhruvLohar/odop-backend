from django.contrib import admin
from .models import User

from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    readonly_fields = ('id', 'access_token', 'created_at', 'modified_at',)
    
    fieldsets = (
        (None, {'fields': ('id', 'is_active',)}),
        ('Personal Information', {
            'fields': ('profile_image', 'name', 'phone_number', 'email', 'gender',)
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code',)
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
    
