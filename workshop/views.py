from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from odop_backend.responses import *
from odop_backend.permissions import CookieAuthentication

class WorkshopAPIView(
    ModelViewSet
):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class EventAPIView(
    ModelViewSet
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]