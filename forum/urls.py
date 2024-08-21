from rest_framework.routers import DefaultRouter
from .views import ForumAPIView

router = DefaultRouter()
router.register(r'', ForumAPIView)