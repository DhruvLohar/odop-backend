from rest_framework.decorators import action

from .models import *
from .serializers import *

from odop_backend.responses import *

class NormalServicesMixin:
    @action(detail=False, methods=['POST'])
    def feedback(self, request):
        message = request.data.get("feedback_message")
        
        feedback = Feedback.objects.create(user=request.user, feedback_message=message)
        feedback.save()
        
        return ResponseSuccess({}, message="Feedback submitted successfully")
    
    @action(detail=False, methods=['GET'])
    def allNotifications(self, request):
        
        notifications = request.user.all_notifications.all()
        serializer = NotificationSerializer(notifications, many=True, context=dict(request=request))
        
        return ResponseSuccess({
            "all_notifications": serializer.data
        }, message="Success")