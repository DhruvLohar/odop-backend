from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

class ForumAPIView(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    