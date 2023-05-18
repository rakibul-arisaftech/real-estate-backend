from . import views
from django.urls import path

urlpatterns = [
    path('category', views.category_list),
    path('category/<int:id>', views.category_detail),
]