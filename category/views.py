from rest_framework import permissions, status, viewsets
from .models import Category
from .serializers import CategoryReadSerializer, CategoryWriteSerializer
from .permissions import IsAuthorOrReadOnly



class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD property
    """

    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CategoryWriteSerializer

        return CategoryReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
