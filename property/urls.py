from . import views
from django.urls import path

urlpatterns = [
    path('property', views.property_list),
    path('property/<int:id>', views.property_detail),
]