from rest_framework import viewsets
from django.utils import timezone
from rest_framework.decorators import action
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string

from .models import Artisan
from .serializers import *

from odop_backend import settings
from odop_backend.permissions import CookieAuthentication
from odop_backend.responses import *

class AuthMixin:
    
    def get_otp_on_phone():
        pass
    
    def get_otp_on_email(subject, template_name, email_to, context=None):
        email_template = render_to_string(f'{template_name}', context if not context else {})
        template_content = html.strip_tags(email_template)
        email = EmailMultiAlternatives(subject, template_content, settings.EMAIL_HOST_USER, to=[email_to])
        email.attach_alternative(email_template, 'text/html')
        email.send()
    
    def create(self, request):
        phone_number = request.data.get("phone_number")
        
        try:
            user = Artisan.objects.get(phone_number=phone_number)
                
            accessToken, changeUserToken = user.generateToken()
            if changeUserToken:
                user.access_token = accessToken
                
            user.last_login = timezone.now()
            user.save()
            
            return ResponseSuccess(response={
                "artisan": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image and request else None,
                    "access_token": user.access_token
                }
            }, message="User Login Successful")
        except Artisan.DoesNotExist:
            try:
                with transaction.atomic():
                    user = Artisan.objects.create(phone_number=phone_number)
                    accessToken, changeUserToken = user.generateToken()
                    if changeUserToken:
                        user.access_token = accessToken
                    
                    user.last_login = timezone.now()
                    user.save()
                
                return ResponseSuccess(response={
                    "user": {
                        "id": user.id,
                        "access_token": user.access_token
                    }
                }, message="User logged in successfully")
            except IntegrityError:
                return ResponseError(message="User with the same 'phone_number' already exists")
            except UnicodeDecodeError as e:
                return ResponseError(message="UnicodeDecodeError occurred: " + str(e))
            except Exception as e:
                return ResponseError(message="An unexpected error occurred: " + str(e))
    

class ArtisanAPIView(
    AuthMixin,
    viewsets.ModelViewSet
):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    authentication_classes = [CookieAuthentication]

    def get_authenticators(self):
        if self.action == 'create':
            return []
        return super().get_authenticators()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        
        return super().perform_destroy(instance)

    @action(detail=False, methods=['PUT'])
    def updateFcmToken(self, request):
        fcm_token = request.data.get("fcm_token")
        
        request.user.fcm_token = fcm_token
        request.user.save()
        
        return ResponseSuccess({}, message="Token updated successfully")
        