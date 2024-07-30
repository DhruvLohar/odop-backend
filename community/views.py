from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

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
    
    
class RentalMachineAPIView(
    ModelViewSet
):
    queryset = RentalMachine.objects.all()
    serializer_class = RentalMachineSerializer
    authentication_classes = [CookieAuthentication]