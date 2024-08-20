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
    
    @action(detail=True, methods=['GET'], authentication_classes=[])
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
    
    @action(detail=True, methods=['POST'], authentication_classes=[])
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
                    "role": "artisan",
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "verified_by_authority": user.verified_by_authority,
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
            
            return ResponseSuccess(response={
                "verified": user.is_active,
                "id": user.id
            }, message="User Login Successful")
            
        except Artisan.DoesNotExist:
            return ResponseError(message="Artisan doesnt exists, please register first.")
        
    @action(detail=False, methods=['POST'], authentication_classes=[])
    def createArtisan(self, request):
        
        email = request.data.get("email")
        
        try:
            artisan = Artisan.objects.get(email=email)
            
            if not artisan.verified_by_authority:
                return ResponseSuccess(response={
                    "id": artisan.id
                })        
        
            return ResponseError("Artisan with that email or phone number already exists.")
        except Artisan.DoesNotExist as e:
            artisan = Artisan.objects.create(email=email)
            artisan.is_active = False
            artisan.save()
            
            return ResponseSuccess(response={
                "id": artisan.id
            })
    
    @action(detail=True, methods=['POST'], authentication_classes=[])
    def registerArtisan(self, request, pk=None):
        print(request.data)
        
        artisan = self.get_object()
        serializer = RegisterArtisanSerializer(artisan, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            
            return ResponseSuccess(
                response={
                    "artisan": serializer.data
                },
                message="Artisan registered successfully"
            )
        
        print(serializer.errors)
        return ResponseError(message="something went wrong")
    

class ArtisanAPIView(
    ModelViewSet,
    AuthMixin,
    ArtisanServicesMixin
):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    authentication_classes = [CookieAuthentication]
    
    def create(self, request, *args, **kwargs):
        return ResponseSuccess(message="not implemented")

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
        
    @action(detail=True, methods=['GET'])
    def getAllProducts(self, request, pk=None):
        artisan = self.get_object()
        
        serializer = ProductSerializer(artisan.listed_products.all(), many=True)
        
        return ResponseSuccess({
            "products": serializer.data
        })
        
    @action(detail=True, methods=['GET'])
    def getAllOrders(self, request, pk=None):
        artisan = self.get_object()
        
        
        artisan_products = [x.id for x in artisan.listed_products.all()]
        line_items = OrderLineItem.objects.filter(product__id__in=artisan_products)
        
        artisan_orders = [x.order for x in line_items]
        
        serializer = OrderSerializer(artisan_orders, many=True)
        
        return ResponseSuccess(response={
            "orders": serializer.data
        })