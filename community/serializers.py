from rest_framework import serializers
from .models import *

from services.models import RentalMachineImage

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class JobPostApplicationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostApplicationRequest
        fields = '__all__'

class RentalMachineSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = RentalMachine
        fields = '__all__'
        
    def get_images(self, instance):
        data = []
        for image in instance.machine_images.all():
            data.append(image.image.url)
        return data

class RentalMachineBookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalMachineBookingRequest
        fields = '__all__'


class JobPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['artisan', 'title', 'description', 'vacancy', 'prerequisites']

class RentalMachineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalMachine
        fields = ['artisan', 'title', 'description', 'starting_time', 'ending_time']
    
    def validate(self, data):
        if data['starting_time'] >= data['ending_time']:
            raise serializers.ValidationError("Ending time must be after starting time.")
        return data
    
    def create(self, validated_data):
        machine = super().create(validated_data)

        machine_images = self.context.get("machine_images")
        
        for imageObj in machine_images:
            image = RentalMachineImage.objects.create(machine=machine, image=imageObj)
            image.save()
        
        return machine