from .serializers import PropertyReadSerializer, PropertyWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly
from .models import Property


class PropertyViewPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 15

class PropertyViewSet(viewsets.ModelViewSet):
    """
    CRUD property
    """

    queryset = Property.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('location', 'price')
    pagination_class = PropertyViewPagination

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



# class PropertySearch(generics.ListAPIView):
#     queryset = Property.objects.all()
#     serializer_class = PropertyReadSerializer
#     filter_backends = (DjangoFilterBackend, SearchFilter)
#     filterset_fields = ('location', 'price')