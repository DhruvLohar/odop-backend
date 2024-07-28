import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from rest_framework_simplejwt.tokens import AccessToken, TokenError

# from firebase_admin import messaging, _messaging_utils
# from service import models as serviceModels

class UserManager(BaseUserManager):
    def create_user(self, contact_number, **extra_fields):
        """
        Creates and saves a user with the given contact number.
        """
        if not contact_number:
            raise ValueError('The contact number must be set.')

        user = self.model(contact_number=contact_number, **extra_fields)
        user.set_unusable_password()  # Set an unusable password since we don't need one
        user.save(using=self._db)
        return user
    
    def create_superuser(self, contact_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(contact_number, password=password, **extra_fields)


def validate_phone_number(value):
    phone_number_pattern = re.compile(r'^\d{4,15}$')
    if not phone_number_pattern.match(value):
        raise ValidationError('Invalid phone number format.')
    
class BaseUser(AbstractBaseUser, models.Model):
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    
    name = models.CharField(max_length=120, blank=True)
    
    email = models.EmailField(null=True, blank=True)
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
    
    access_token = models.TextField(null=True, blank=True)
    fcm_token = models.TextField(null=True, blank=True)
    
    # objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']
    
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
    
    # def sendNotification(self, payload, sent_by, noti_type):
    #     notification_details = payload.get("notification", {})
    #     data = payload.get("data", {})
        
    #     title = notification_details.get("title")
    #     body = notification_details.get("body")
        
    #     # Ensure title and body are not None
    #     if not title:
    #         print("Notification title is missing.")
    #         return None
        
    #     existing_notification = serviceModels.Notification.objects.filter(
    #         notification_type=noti_type,
    #         user=self,
    #         sender_user=sent_by,
    #         is_valid=True
    #     )
        
    #     if existing_notification.exists():
    #         existing_notification.update(is_valid=False)
        
    #     # Create the notification in our database
    #     notification = serviceModels.Notification.objects.create(
    #         notification_type=noti_type,
    #         title=title,
    #         user=self,
    #         sender_user=sent_by
    #     )
        
    #     if not notification:
    #         print("Failed to create notification in the database.")
    #         return None
            
    #     # Prepare the message
    #     base_data = {
    #         "id": str(sent_by.id),
    #         "notification_id": str(notification.id),
    #         "type": noti_type
    #     }
    #     base_data.update(data)
        
    #     payload["data"] = base_data
    #     notification.payload = payload
    #     notification.save()
        
    #     if self.fcm_token:
    #         try:
    #             message = messaging.Message(
    #                 data=base_data,
    #                 notification=messaging.Notification(
    #                     title=title,
    #                     body=body
    #                 ),
    #                 token=self.fcm_token
    #             )
    #             # Attempt to send the message
    #             response = messaging.send(message)
    #             return notification
    #         except _messaging_utils.UnregisteredError:
    #             print(f"Token {self.fcm_token} is unregistered. Removing from database.")
    #         except Exception as e:
    #             print(f"Error sending notification: {e}")
                
    #     return notification

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