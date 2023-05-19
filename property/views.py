from rest_framework import permissions, status, viewsets
from .models import Property
from .serializers import PropertyReadSerializer, PropertyWriteSerializer
from .permissions import IsAuthorOrReadOnly



class PropertyViewSet(viewsets.ModelViewSet):
    """
    CRUD property
    """

    queryset = Property.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PropertyWriteSerializer

        return PropertyReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
