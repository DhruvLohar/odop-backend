from rest_framework.routers import DefaultRouter
from .views import *

workshopRouter = DefaultRouter()
workshopRouter.register(r'', WorkshopAPIView, basename='workshop')


eventRouter = DefaultRouter()
eventRouter.register(r'', EventAPIView, basename='event')