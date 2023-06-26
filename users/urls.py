from users import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register(r"wishlist", views.WishlistViewSet)

urlpatterns = [
    path("health", views.health_check),
    # path("register", views.UserRegistrationAPIView.as_view(), name="create-user"),
    # path("login", views.UserLoginAPIView.as_view(), name="login-user"),
    # path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    # path("logout", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("", include(router.urls)),
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginAPIView.as_view(), name="login"),
    path('logout', views.LogoutAPIView.as_view(), name="logout"),
    path('email-verify', views.VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
]