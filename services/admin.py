from django.contrib import admin
from .models import *

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_message',)
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at',)
    
@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'star_rating', 'comment',)
    

class RentalMachineImageInline(admin.TabularInline):
    model = RentalMachineImage
    extra = 1  # Number of extra blank forms to display
    fields = ['image']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra blank forms to display
    fields = ['image']
    
class WorkshopImageInline(admin.TabularInline):
    model = WorkshopImage
    extra = 1  # Number of extra blank forms to display
    fields = ['image']