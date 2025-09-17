from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserProfileViewSet,
    RegisterPage, LoginPage, LogoutPage
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    # --- API Endpoints ---
    path("api/register/", RegisterView.as_view(), name="register-api"),
    path("api/login/", TokenObtainPairView.as_view(), name="login-api"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh-api"),
    path("api/", include(router.urls)),

    # --- Web Pages ---
    path("register/", RegisterPage.as_view(), name="register-page"),
    path("login/", LoginPage.as_view(), name="login-page"),
    path("logout/", LogoutPage.as_view(), name="logout-page"),
]
