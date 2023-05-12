from django.urls import path
from . import views

urlpatterns = [
    path('property', views.property_list),
    path('property/<int:id>', views.property_detail),
]