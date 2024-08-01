from rest_framework import serializers
from .models import *

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

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

