from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, HealthProgramViewSet, home, register_client, client_list, enroll_client
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'programs', HealthProgramViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_client, name='register_client'),
    path('clients/', views.client_list, name='client_list'),
    path('enroll/<int:client_id>/', views.enroll_client, name='enroll_client'),
]
