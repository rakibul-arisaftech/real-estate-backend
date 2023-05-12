from django.urls import path
from . import views

urlpatterns = [
    path('category', views.category_list),
    path('category/<int:id>', views.category_detail),
]