from . import views
from django.urls import path

urlpatterns = [
    path('service/create', views.create_service),
    path('service/services', views.get_services),
    path('service/<int:id>', views.get_service),
    path('service/update/<int:id>', views.update_service),
    path('service/delete/<int:id>', views.delete_service),
]