from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

app_name = "category"

router = DefaultRouter()
router.register(r"^(?P<post_id>\d+)/", CategoryViewSet)
router.register(r"category", CategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
]