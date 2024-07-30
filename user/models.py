import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser

from services.models import Notification

from rest_framework_simplejwt.tokens import AccessToken, TokenError

from firebase_admin import messaging, _messaging_utils

def validate_phone_number(value):
    phone_number_pattern = re.compile(r'^\d{4,15}$')
    if not phone_number_pattern.match(value):
        raise ValidationError('Invalid phone number format.')
    
class BaseUser(AbstractBaseUser, models.Model):
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    
    name = models.CharField(max_length=120, blank=True)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,  # Adjust length as needed
        unique=True,
        validators=[validate_phone_number]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    
    valid_otp = models.PositiveIntegerField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    fcm_token = models.TextField(null=True, blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']
    
    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"

    def generateToken(self):
        """
        return: token, need_for_updation
        """
        try:
            token = AccessToken(self.access_token)

            if self.access_token is not None:
                return str(self.access_token), False
        except TokenError as e:
            pass

        new_token = AccessToken.for_user(self)
        return str(new_token), True
    
    def sendNotification(self, title, body):
        
        # Create the notification in our database
        notification = Notification.objects.create(
            user=self.pk,
            title=title,
            body=body
        )
        notification.save()
        
        if not notification:
            print("Failed to create notification in the database.")
            return None
        
        if self.fcm_token:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    token=self.fcm_token
                )
                # Attempt to send the message
                response = messaging.send(message)
                
            except _messaging_utils.UnregisteredError:
                print(f"Token {self.fcm_token} is unregistered. Removing from database.")
            except Exception as e:
                print(f"Error sending notification: {e}")
                
        return notification

    def __str__(self):
        return str(self.name)
    
    
GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class User(BaseUser):
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    
    address = models.TextField(null=True, blank=True) 
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return str(self.name)