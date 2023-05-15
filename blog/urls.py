from . import views
from django.urls import path

urlpatterns = [
    path('blog/post', views.post_list),
    path('blog/post/<int:id>', views.post_detail),
    path('blog/comment', views.comment_list),
    path('blog/comment/<int:id>', views.comment_detail),
]