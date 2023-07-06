from users import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register(r"wishlist", views.WishlistViewSet)

urlpatterns = [
    path("health", views.health_check),
    path("register", views.UserRegistrationAPIView.as_view(), name="create-user"),
    path("login", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("email-verify", views.VerifyEmailOTP.as_view(), name='email-verify'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('reset-password', views.ResetPasswordOTP.as_view(), name='reset-password'),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("", include(router.urls)),
]