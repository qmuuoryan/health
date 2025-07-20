from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, HealthProgramViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'programs', HealthProgramViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
