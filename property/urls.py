from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, LatestPropertyView

app_name = "property"

router = DefaultRouter()
router.register(r"^(?P<post_id>\d+)/", PropertyViewSet)
router.register(r"property", PropertyViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("property/latest", LatestPropertyView.as_view()),
]