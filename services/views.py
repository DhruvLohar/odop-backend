from rest_framework.decorators import action

from .models import *
from .serializers import *
from .tasks import *

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
        

class ArtisanServicesMixin:
    @action(detail=False, methods=['POST'])
    def getChatbotResponse(self, request):
        
        prompt = request.data.get("prompt")
        
        # resp = get_chatbot_response(prompt)
        
        return ResponseSuccess({
            "type": "response",
            "content": "Blah blah blah",
            "payload": []
        })
    
    @action(detail=False, methods=['POST'])
    def verifyDocuments(self, request):
        
        # image = request.data.get("image")
        # 
        # print(image)
        # hello_world.delay()
        
        return ResponseSuccess(message="response 1")
    
    @action(detail=False, methods=['POST'])
    def getForecastingData(self, request):
        
        raw_material = request.data.get("raw_material")
        
        print(raw_material)
        
        return ResponseSuccess(message="response 1")