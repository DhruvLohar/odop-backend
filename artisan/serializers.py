from rest_framework import serializers
from .models import Artisan

class ArtisanSerializer(serializers.ModelSerializer):
    
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Artisan
        fields = ('id', 'name', 'phone_number', 'profile_image',)
        
    def get_profile_image(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.profile_image.url) if instance.profile_image and request else None   

class UpdateArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisan
        fields = (
            'id', 'name', 'phone_number', 'profile_image',
        )

class CreateArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisan
        fields = ['name', 'phone_number']