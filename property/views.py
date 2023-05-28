from .serializers import PropertyReadSerializer, PropertyWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.decorators import api_view
from .permissions import IsAuthorOrReadOnly
from .models import Property
from rest_framework.views import APIView


class LatestPropertyView(APIView):
    def get(self, request, format=None):
        queryset = Property.objects.order_by('-id')[:6]
        serializer = PropertyReadSerializer(queryset, context={"request": 
                        request}, many=True)
        return Response(serializer.data)


# @api_view(['GET'])
# def latest_property(request):
#     if request.method == 'GET':
#         properties = Property.objects.order_by('-id')[0:6]
#         serializer = PropertyReadSerializer(properties, context={"request": request}, many=True)
#         return Response(serializer.data)



class PropertyViewPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 15

class PropertyViewSet(viewsets.ModelViewSet):
    """
    CRUD property
    """

    queryset = Property.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('location', 'property_type', 'price')
    pagination_class = PropertyViewPagination

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PropertyWriteSerializer

        return PropertyReadSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     # Add any additional context data you want to pass to the serializer
    #     context['request'] = self.request
    #     return context
    
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