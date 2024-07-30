from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.authentication import JWTAuthentication

from odop_backend import settings
from artisan.models import Artisan
from user.models import BaseUser

class IsArtisan(permissions.BasePermission):
    message = "You cannot perform this action"

    def has_permission(self, request, view):
        return request.user_type == "artisan"

class UserObjectPermission(permissions.BasePermission):
    message = 'You do not have Object permission to perform this action.'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the access token from the cookie
        access_token = self.get_access_token(request)

        if not access_token:
            return None

        # Validate and decode the access token
        validated_token = self.get_validated_token(access_token)

        try:
            # Retrieve the user based on the token's user_id
            user = BaseUser.objects.get(id=validated_token[settings.SIMPLE_JWT.get('USER_ID_CLAIM')])
            
            request.user_type = self.get_user_type(user)

            # Return a tuple of (user, validated_token) to indicate a successful authentication
            return (user, validated_token)

        except BaseUser.DoesNotExist:
            # If the user is not found, raise an AuthenticationFailed exception
            raise AuthenticationFailed('User not found')

    def get_access_token(self, request):
        # Get the access token from the cookie
        try:
            cookie_name = self.get_cookie_name()
            authorization_header = get_authorization_header(request).decode('utf-8')
            auth_header_prefix = self.get_header_prefix().lower()

            if authorization_header and authorization_header.lower().startswith(auth_header_prefix):
                auth_token = authorization_header.split()[1]

                if auth_token != 'null':
                    return auth_token

            if cookie_name in request.COOKIES:
                return request.COOKIES[cookie_name]

            return None
        except Exception: return None
        
    @staticmethod
    def get_user_type(user):
        try:
            a = Artisan.objects.get(id=user.id)
            return "artisan" 
        except Exception:
            return "user"

    def get_cookie_name(self):
        return settings.SIMPLE_JWT.get('ACCESS_TOKEN_COOKIE_NAME')

    def get_header_prefix(self):
        return 'Bearer'
