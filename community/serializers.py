from rest_framework import serializers
from .models import *

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class JobPostApplicationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostApplicationRequest
        fields = '__all__'

class RentalMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalMachine
        fields = '__all__'

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
