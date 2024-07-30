from django.utils import timezone

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    user = models.ForeignKey("user.BaseUser", related_name='app_feedbacks', on_delete=models.PROTECT)
    feedback_message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.user.name)
    

class Notification(models.Model):

    user = models.ForeignKey("user.BaseUser", related_name='all_notifications', on_delete=models.PROTECT)
    
    title = models.CharField(max_length=250)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.user.name)
    

class OrderReview(models.Model):
    
    order = models.ForeignKey("order.Order", related_name="user_reviews", on_delete=models.PROTECT)
    reviewer = models.ForeignKey("user.User", related_name='order_reviews', on_delete=models.PROTECT)
    
    star_rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    comment = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user.name} # {self.order}"
    
    def canReviewOrder(self, uid):
        return self.order.user.pk == int(uid)
            