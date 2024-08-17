from rest_framework import serializers
from .models import *
from services.models import WorkshopImage

class WorkshopSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Workshop
        fields = '__all__'
        
    def get_images(self, instance):
        data = []
        
        for image in instance.workshop_images.all():
            data.append(image.image.url)

        return data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class WorkshopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['title', 'description', 'address', 'date', 'workshop_level', 'tags', 'organized_by', 'conducted_by_artisan', 'artisan', 'price']

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'address', 'date', 'tags']
        
    def create(self, validated_data):
        workshop = super().create(validated_data)

        workshop_images = self.context.get("workshop_images")
        
        for imageObj in workshop_images:
            image = WorkshopImage.objects.create(workshop=workshop, image=imageObj)
            image.save()
        
        return workshop

