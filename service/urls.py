from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ServiceViewSet

app_name = "service"

router = DefaultRouter()
router.register(r"^(?P<post_id>\d+)/", ServiceViewSet, 'service-crud')
router.register(r"service", ServiceViewSet, 'create-service')


urlpatterns = [
    path("", include(router.urls)),
]