from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'profile_image',)
        
    def get_profile_image(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.profile_image.url) if instance.profile_image and request else None   

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'phone_number', 'profile_image',)

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number']