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
        
class RegisterArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisan
        fields = [
            'name', 'email', 'phone_number', 'gender', 'age',
            'state', 'district', 'address', 'postal_code',
            'aadhar_image', 'pan_image' 
        ]
    
    def create(self, validated_data):
        artisan: Artisan = super().create(validated_data)
        
        artisan.is_active = True
        artisan.verified_by_authority = True
        artisan.save()
        
        return artisan
    
    def update(self, instance, validated_data):
        artisan: Artisan = super().update(instance, validated_data)
        
        artisan.verified_by_authority = True
        artisan.save()
        
        return artisan