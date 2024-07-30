from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from odop_backend.responses import *
from odop_backend.permissions import CookieAuthentication, IsArtisan

class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user_type == "artisan":
            return NotAuthorized()
        
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = OrderCreateSerializer(data=data, context=dict(
            order_lines=request.data.pop("order_lines")
        ))
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return ResponseSuccess({
            "order": serializer.data
        })
    
    @action(detail=False, methods=['POST'])
    def updateStatus(self, request):
        
        orderLineItemId = request.data.get("orderLineItemId")
        status = request.data.get("status")
        estimated_time = request.data.get("estimated_time")
        
        try:
            orderLineItem = OrderLineItem.objects.get(id=orderLineItemId)
            
            if request.user_type != "artisan" and orderLineItem.product.artisan.id != request.user.id:
                return NotAuthorized()
            
            statuses = [x[0] for x in ORDER_STATUS]
            if not status in statuses:
                return ResponseError(message="Invalid status")
            
            if estimated_time:
                orderLineItem.estimate_delivery_time = estimated_time
            orderLineItem.status = status
            orderLineItem.save()
            
            return ResponseSuccess(message="Status Updated Successfully")
        except OrderLineItem.DoesNotExist:
            return ResponseError("Order Item not found")
        
    