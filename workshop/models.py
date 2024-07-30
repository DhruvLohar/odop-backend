from django.db import models

WORKSHOP_LEVEL = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advance', 'Advance'),
)

class Workshop(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    address = models.TextField()
    date = models.DateTimeField()
    
    workshop_level = models.CharField(choices=WORKSHOP_LEVEL, max_length=50)
    tags = models.JSONField(default=list)
    
    organized_by = models.CharField(max_length=200)
    conducted_by_artisan = models.BooleanField(default=False)
    artisan = models.ForeignKey("artisan.Artisan", related_name="conducted_workshops", on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class Event(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    address = models.TextField()
    date = models.DateTimeField()
    
    tags = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
