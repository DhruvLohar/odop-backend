from rest_framework import serializers
from .models import *
from services.models import WorkshopImage

from artisan.serializers import ArtisanSerializer

class WorkshopSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField()
    artisan = ArtisanSerializer()
    
    class Meta:
        model = Workshop
        fields = '__all__'
        
    def get_images(self, instance):
        data = []
        
        for image in instance.workshop_images.all():
            data.append(image.image.url)

        return data

class EventSerializer(serializers.ModelSerializer):
    artisan = ArtisanSerializer()
        
    class Meta:
        model = Event
        fields = '__all__'

class NoValidationListField(serializers.ListField):
    def to_internal_value(self, data):
        # Bypass default validation and directly return the data
        return data

class WorkshopCreateSerializer(serializers.ModelSerializer):
    tags = NoValidationListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Workshop
        fields = ['title', 'description', 'address', 'date', 'workshop_level', 'tags', 'conducted_by_artisan', 'artisan', 'price', 'is_active']

    def create(self, validated_data):
        workshop = super().create(validated_data)
        
        workshop_images = self.context.get("workshop_images")
        tags = self.context.get("tags")
        
        workshop.tags = tags
        workshop.save()
        
        for imageObj in workshop_images:
            image = WorkshopImage.objects.create(workshop=workshop, image=imageObj)
            image.save()
        
        return workshop

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'address', 'date', 'tags']

