from django.contrib import admin
from .models import Forum

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')