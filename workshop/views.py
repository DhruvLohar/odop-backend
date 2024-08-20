from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from user.models import User
from artisan.models import Artisan

from odop_backend.responses import *
from odop_backend.permissions import CookieAuthentication

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Workshop
from .serializers import WorkshopSerializer
from artisan.models import Artisan
from user.models import User
from odop_backend.responses import ResponseSuccess, ResponseError
from odop_backend.permissions import CookieAuthentication

class WorkshopAPIView(ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["artisan"] = request.user.id
        data["conducted_by_artisan"] = True
        
        tags = []

        if "tags" in data and isinstance(data["tags"], str):
            tags = [tag.strip() for tag in data["tags"].split(",")]
            

        serializer = WorkshopCreateSerializer(data=data, context={
            "workshop_images": request.data.getlist('workshop_images[]'),
            "tags": tags 
        })
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)

            return ResponseSuccess(response={
                "workshop": serializer.data
            }, message="Workshop has been created")
            
        print(serializer.errors)
        return ResponseError("something went wrong")

    def list(self, request, *args, **kwargs):
        queryset = Workshop.objects.filter(is_active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ResponseSuccess(response={
            "workshops": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        workshop = self.get_object()
        serializer = self.get_serializer(workshop)
        return ResponseSuccess(response={
            "workshop": serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        workshop = self.get_object()
        if workshop.artisan.id != request.user.id:
            return ResponseError(message="You are not authorized to update this workshop.")

        serializer = self.get_serializer(workshop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return ResponseSuccess(response={
            "workshop": serializer.data
        }, message="Workshop has been updated")

    def destroy(self, request, *args, **kwargs):
        workshop = self.get_object()
        if workshop.artisan.id != request.user.id:
            return ResponseError(message="You are not authorized to delete this workshop.")

        workshop.is_active = False
        workshop.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def get_all_from_district(self, request):
        district = request.query_params.get("district")
        if not district:
            return ResponseError(message="District parameter is required.")

        workshops = Workshop.objects.filter(address__icontains=district, is_active=True)
        serializer = self.get_serializer(workshops, many=True)
        return ResponseSuccess(response={
            "workshops": serializer.data
        })

    @action(detail=True, methods=['POST'])
    def apply(self, request, pk=None):
        workshop = self.get_object()
        
        return ResponseSuccess(message="Applied to the workshop successfully")

    
class EventAPIView(ModelViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return ResponseSuccess(response={
            "event": serializer.data
        }, message="Event has been created")

    def list(self, request, *args, **kwargs):
        queryset = Event.objects.filter(is_active=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ResponseSuccess(response={
            "events": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        
        if not event.is_active:
            return ResponseError(message="Event not found", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event)
        return ResponseSuccess(response={
            "event": serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        event = self.get_object()
        if not event.is_active:
            return ResponseError(message="Event not found", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return ResponseSuccess(response={
            "event": serializer.data
        }, message="Event has been updated")

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if not event.is_active:
            return ResponseError(message="Event not found", status=status.HTTP_404_NOT_FOUND)

        event.is_active = False
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def get_all_from_district(self, request):
        district = request.query_params.get("district")
        if not district:
            return ResponseError(message="District parameter is required.")

        events = Event.objects.filter(address__icontains=district, is_active=True)
        serializer = self.get_serializer(events, many=True)
        return ResponseSuccess(response={
            "events": serializer.data
        })

    @action(detail=True, methods=['POST'])
    def register(self, request, pk=None):
        event = self.get_object()
        if not event.is_active:
            return ResponseError(message="Event not found", status=status.HTTP_404_NOT_FOUND)

       
        return ResponseSuccess(message="Registered to the event successfully")