from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=60)
    post_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    tags = models.CharField(max_length=40)
    fb = models.CharField(max_length=254)
    twitter = models.CharField(max_length=254)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s comment on {self.post.title}"

    