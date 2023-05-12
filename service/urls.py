from django.urls import path
from . import views

urlpatterns = [
    path('service', views.service_list),
    path('service/<int:id>', views.service_detail),
]