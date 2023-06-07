from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, LatestPropertyView, CommentViewSet

app_name = "property"

router = DefaultRouter()
router.register(r"", PropertyViewSet)
router.register(r"^(?P<post_id>\d+)/", PropertyViewSet)
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("latest", LatestPropertyView.as_view()),
]