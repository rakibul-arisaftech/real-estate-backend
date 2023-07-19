from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, LatestPropertyView, CommentViewSet

app_name = "property"

router = DefaultRouter()
router.register(r"^property", PropertyViewSet)
router.register(r"^property/(?P<post_id>\d+)/", PropertyViewSet)
router.register(r"^property/(?P<post_id>\d+)/comment", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("property/latest", LatestPropertyView.as_view()),
]