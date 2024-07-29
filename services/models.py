from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError
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