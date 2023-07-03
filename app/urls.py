from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('profile/', views.ProfileApi.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('verify/', TokenVerifyView.as_view(), name="verify"),
]
