from random import randint
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework.decorators import action
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string

from .models import Artisan
from .serializers import *
from order.models import OrderLineItem
from product.serializers import *
from order.serializers import *
from services.views import ArtisanServicesMixin

from odop_backend import settings
from odop_backend.permissions import CookieAuthentication
from odop_backend.responses import *

class AuthMixin:
    
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
        
        try:
            user = Artisan.objects.get(email=email)
            
            if not user.is_active:
                return ResponseSuccess(response={
                    "verified": False,
                    "artisan": {
                        "id": user.id
                    }
                })
                
            if not user.verified_by_authority:
                return ResponseSuccess(response={
                    "authority_verified": False,
                    "artisan": {
                        "id": user.id,
                    }
                })
            
            accessToken, changeUserToken = user.generateToken()
            if changeUserToken:
                user.access_token = accessToken
                
            user.last_login = timezone.now()
            user.save()
            
            return ResponseSuccess(response={
                "verified": True,
                "artisan": {
                    "id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image and request else None,
                    "access_token": user.access_token
                }
            }, message="User Login Successful")
        except Artisan.DoesNotExist:
            try:
                with transaction.atomic():
                    serializer = CreateArtisanSerializer(data=request.data)
                    
                    if serializer.is_valid(raise_exception=False):
                        serializer.save()
                        
                        user = Artisan.objects.get(email=serializer.data.get("email"))
                        user.is_active = False
                        user.save()
                    
                        return ResponseSuccess(response={
                            "verified": False,
                            "artisan": {
                                "id": user.id
                            }
                        }, message="Artisan logged in successfully")
                    
                    return ResponseError(message="Something went wrong while creating an artisan")
                    
            except IntegrityError:
                return ResponseError(message="artisan with the same 'email' already exists")
            except UnicodeDecodeError as e:
                return ResponseError(message="UnicodeDecodeError occurred: " + str(e))
            except Exception as e:
                return ResponseError(message="An unexpected error occurred: " + str(e))
    

class ArtisanAPIView(
    ModelViewSet,
    AuthMixin,
    ArtisanServicesMixin
):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    authentication_classes = [CookieAuthentication]

    # def get_authenticators(self):
    #     if self.action == 'create':
    #         return []
    #     return super().get_authenticators()

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
    
    @action(detail=True, methods=['GET'])
    def getAllProducts(self, request, pk=None):
        artisan = self.get_object()
        
        products = artisan.listed_products.all()
        serializer = ProductSerializer(products, many=True)
        
        return ResponseSuccess({
            "products": serializer.data
        })
        
    @action(detail=True, methods=['GET'])
    def allPendingOrders(self, request, pk=None):
        artisan = self.get_object()
        
        order_lines = OrderLineItem.objects.filter(product__artisan__id=artisan.id)
        serializer = ArtisanOrdersListSerializer(order_lines, many=True)
        
        return ResponseSuccess({
            "orders": serializer.data
        })