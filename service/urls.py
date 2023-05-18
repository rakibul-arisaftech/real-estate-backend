from . import views
from django.urls import path

urlpatterns = [
    path('service', views.service_list),
    path('service/<int:id>', views.service_detail),
]