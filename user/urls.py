from rest_framework.routers import DefaultRouter
from .views import UserAPIView

router = DefaultRouter()
router.register(r'', UserAPIView, basename='user')
