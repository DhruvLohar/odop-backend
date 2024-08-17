from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from odop_backend.responses import *
from odop_backend.permissions import CookieAuthentication, IsArtisan

class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsArtisan()]
        
        return super().get_permissions()
    
    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Product.objects.filter(is_verified=True)
        
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        data["artisan"] = request.user.id
        
        serializer = ProductCreateSerializer(data=data, context={
            "product_images": request.data.getlist('product_images[]')
        })
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return ResponseSuccess(response={
            "product": serializer.data
        })