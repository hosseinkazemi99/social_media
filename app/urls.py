from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from .views import SubscribeApi, SubscribeDetailApi, PostApi, PostDetailApi

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('verify/', TokenVerifyView.as_view(), name="verify"),
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('profile/', views.ProfileApi.as_view(), name='profile'),
    path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
    path("subscribe/<str:email>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
    path("post/", PostApi.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
]
