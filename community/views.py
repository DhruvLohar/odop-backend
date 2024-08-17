from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import *
from .serializers import *

from odop_backend.responses import *
from odop_backend.permissions import CookieAuthentication

class JobPostAPIView(
    ModelViewSet
):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        
        data = request.data.copy()
        data["artisan"] = request.user.id
        
        serializer = JobPostCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        return ResponseSuccess(response={
            "job_post": serializer.data
        }, message="Job post has been created")
    
    
    def list(self, request, *args, **kwargs):
        queryset = JobPost.objects.filter(
            is_active=True
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ResponseSuccess(response={
            "job_posts": serializer.data
        })
    
    @action(detail=True, methods=['POST'])
    def apply(self, request, pk=None):
        job_post = self.get_object()
        artisan_id = request.user.id
        about = request.data.get("about")
        
        if job_post.artisan.id == artisan_id:
            return ResponseError(message="You cannot apply for your own job")
        
        serializer = JobPostApplicationRequestSerializer(data={
            "artisan": artisan_id,
            "job_post": job_post.id,
            "about": about
        })
        
        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(response={
                "application": serializer.data
            }, message="Apply hogaya")
        return ResponseError(message="Cannot create application request")
    


    def destroy(self, request, *args, **kwargs):
            job_post = self.get_object()
            if job_post.artisan.id != request.user.id:
                return NotAuthorized()

            job_post.is_active = False
            job_post.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
    

class RentalMachineAPIView(ModelViewSet):
    queryset = RentalMachine.objects.all()
    serializer_class = RentalMachineSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["artisan"] = request.user.id

        serializer = RentalMachineCreateSerializer(data=data, context={
            "machine_images": request.data.getlist('machine_images[]')
        })
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return ResponseSuccess(response={
            "rental_machine": serializer.data
        }, message="Rental machine has been created")
    
    def list(self, request, *args, **kwargs):
        queryset = RentalMachine.objects.filter(is_active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ResponseSuccess(response={
            "rental_machines": serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        rental_machine = self.get_object()
        if rental_machine.artisan.id != request.user.id:
            return NotAuthorized()

        serializer = RentalMachineCreateSerializer(rental_machine, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return ResponseSuccess(response={
            "rental_machine": serializer.data
        }, message="Rental machine has been updated")

    @action(detail=True, methods=['POST'])
    def book(self, request, pk=None):
        rental_machine = self.get_object()
        artisan_id = request.user.id
        start_time_str = request.data.get("start_time")
        end_time_str = request.data.get("end_time")
        purpose = request.data.get("purpose")

        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)

        if not start_time or not end_time:
            return ResponseError(message="Invalid start or end time format.")

        if start_time.tzinfo is None:
            start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
        if end_time.tzinfo is None:
            end_time = timezone.make_aware(end_time, timezone.get_current_timezone())

       
        if rental_machine.artisan.id == artisan_id:
            return ResponseError(message="You cannot book your own rental machine.")

        if not (rental_machine.starting_time <= start_time.time() and rental_machine.ending_time >= end_time.time()):
            return ResponseError(message="The requested time slot is outside of the machine's availability.")

        conflicting_bookings = RentalMachineBookingRequest.objects.filter(
            rental_machine=rental_machine,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='APR' 
        ).exists()

        if conflicting_bookings:
            return ResponseError(message="The requested time slot is already booked.")

        serializer = RentalMachineBookingRequestSerializer(data={
            "artisan": artisan_id,
            "rental_machine": rental_machine.id,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": purpose
        })

        if serializer.is_valid():
            serializer.save()
            return ResponseSuccess(response={
                "booking": serializer.data
            }, message="Booking request has been submitted")
        return ResponseError(message="Cannot create booking request")
    
    def destroy(self, request, *args, **kwargs):
        rental_machine = self.get_object()
        if rental_machine.artisan.id != request.user.id:
            return NotAuthorized()

        rental_machine.is_active = False
        rental_machine.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
