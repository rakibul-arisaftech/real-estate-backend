from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, HealthCheckAPI
from django.urls import path

urlpatterns = [
    path('health', HealthCheckAPI.as_view(), name='health'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
]