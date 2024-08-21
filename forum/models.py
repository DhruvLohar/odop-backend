import uuid
from django.db import models
from django.utils import timezone

class Forum(models.Model):
    
    image = models.ImageField(upload_to="forums/", null=True, blank=True)
    
    slug = models.SlugField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    messages = models.JSONField(default=list, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    def addMessage(self, type: str, sender, message, object_id=None):
        
        type = type.lower()
        avail_type = [
            'message',
            'workshop',
            'event',
            'rental_machines',
            'job_post',
        ]
        
        if type not in avail_type:
            return
        
        msg_payload = dict(
            type=type,
            sender_id=sender, # artisan
            content=message, 
            time=timezone.now().strftime("%H:%M")
        )
        
        if object_id:
            msg_payload.update({"object_id": object_id})
        
        self.messages.append(msg_payload)
        self.save()