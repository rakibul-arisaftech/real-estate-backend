from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CommentViewSet, PostViewSet

app_name = "blog"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)
router.register(r"", PostViewSet)


urlpatterns = [
    path("", include(router.urls)),
]