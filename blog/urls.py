from . import views
from django.urls import path

urlpatterns = [
    path('blog/create', views.create_post),
    path('blog/posts', views.get_posts),
    path('blog/post/<int:id>', views.get_post),
    path('blog/update/<int:id>', views.update_post),
    path('blog/delete/<int:id>', views.delete_post),
]