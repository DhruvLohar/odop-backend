from random import randint
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework.decorators import action
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string

from .models import User
from .serializers import *

from odop_backend import settings
from odop_backend.permissions import CookieAuthentication
from odop_backend.responses import *

class AuthMixin:
    
    def get_otp_on_phone():
        pass
    
    @staticmethod
    def send_otp_on_email(subject, template_name, email_to, context=None):
        try:
            email_template = render_to_string(template_name, context=context if context else {})
            template_content = html.strip_tags(email_template)
            email = EmailMultiAlternatives(subject, template_content, settings.EMAIL_HOST_USER, to=[email_to])
            email.attach_alternative(email_template, 'text/html')
            email.send()
            return True
        except Exception as e:
            print(e)
            return False
    
    @action(detail=True, methods=['GET'])
    def getOTPOnEmail(self, request, pk=None):
        user = self.get_object()
        
        generated_otp = randint(1000, 9999)
        email_sent = self.send_otp_on_email(
            "ODOP | OTP Authentication",
            "otp_email_template.html",
            user.email,
            context={
                "date": timezone.now().strftime("%d %B, %Y"),
                "username": user.name,
                "generated_otp": generated_otp
            }
        )
        
        if email_sent:
            user.valid_otp = generated_otp
            user.save()
            return ResponseSuccess(message="Email was sent on the specified email")
        return ResponseError(message="Something went wrong sending the email")
    
    @action(detail=True, methods=['POST'])
    def verifyOTPOnEmail(self, request, pk=None):
        user = self.get_object()
        entered_otp = request.data.get("otp")
        
        if user.valid_otp == entered_otp:
            accessToken, changeUserToken = user.generateToken()
            if changeUserToken:
                user.access_token = accessToken

            user.is_active = True
            user.last_login = timezone.now()
            user.save()
            
            return ResponseSuccess(response={
                "verified": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image and request else None,
                    "access_token": user.access_token
                }
            }, message="User Login Successful")
        return ResponseError(message="Invalid OTP. Please try again")
    
    @action(detail=False, methods=['POST'], authentication_classes=[])
    def signUpSignIn(self, request):
        email = request.data.get("email")
        print(request.data)
        
        try:
            user = User.objects.get(email=email)
            
            if not user.is_active:
                return ResponseSuccess(response={
                    "verified": False,
                    "user": {
                        "id": user.id
                    }
                })
            
            accessToken, changeUserToken = user.generateToken()
            if changeUserToken:
                user.access_token = accessToken
                
            user.last_login = timezone.now()
            user.save()
            
            return ResponseSuccess(response={
                "verified": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image and request else None,
                    "access_token": user.access_token
                }
            }, message="User Login Successful")
        except User.DoesNotExist:
            try:
                with transaction.atomic():
                    serializer = CreateUserSerializer(data=request.data)
                    
                    if serializer.is_valid(raise_exception=False):
                        serializer.save()
                        
                        user = User.objects.get(email=serializer.data.get("email"))
                        user.is_active = False
                        user.save()
                    
                        return ResponseSuccess(response={
                            "verified": False,
                            "user": {
                                "id": user.id
                            }
                        }, message="User logged in successfully")
                    
                    return ResponseError(message="Something went wrong while creating an user")
                    
            except IntegrityError:
                return ResponseError(message="User with the same 'phone_number' already exists")
            except UnicodeDecodeError as e:
                return ResponseError(message="UnicodeDecodeError occurred: " + str(e))
            except Exception as e:
                return ResponseError(message="An unexpected error occurred: " + str(e))
    

class UserAPIView(
    ModelViewSet,
    AuthMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [CookieAuthentication]

    # def get_authenticators(self):
    #     if self.action in ['create']:
    #         return []
    #     return super().get_authenticators()
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

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
        