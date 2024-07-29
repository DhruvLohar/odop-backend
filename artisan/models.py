from django.db import models
from user.models import BaseUser, GENDER

class Artisan(BaseUser):
    
    verified_by_authority = models.BooleanField(default=False)
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    
    address = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    aadhar_number = models.CharField(max_length=15, null=True, blank=True)
    aadhar_image = models.ImageField(upload_to="artisan/aadhar/")
    
    pan_number = models.CharField(max_length=15, null=True, blank=True)
    pan_image = models.ImageField(upload_to="artisan/panCard/")
    
    class Meta:
        verbose_name = "Artisan"
        verbose_name_plural = "Artisans"
    
    def __str__(self):
        return str(self.name)
