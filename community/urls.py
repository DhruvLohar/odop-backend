from rest_framework.routers import DefaultRouter
from .views import *

jobRouter = DefaultRouter()
jobRouter.register(r'', JobPostAPIView, basename='job-post')


machineRouter = DefaultRouter()
machineRouter.register(r'', RentalMachineAPIView, basename='rental-machine')