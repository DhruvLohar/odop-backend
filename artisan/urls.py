from rest_framework.routers import DefaultRouter
from .views import ArtisanAPIView

router = DefaultRouter()
router.register(r'', ArtisanAPIView, basename='artisan')
