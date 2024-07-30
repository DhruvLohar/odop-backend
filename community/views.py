from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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
        
    
class RentalMachineAPIView(
    ModelViewSet
):
    queryset = RentalMachine.objects.all()
    serializer_class = RentalMachineSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]