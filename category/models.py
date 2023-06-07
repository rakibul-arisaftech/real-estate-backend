from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="category",
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=60)
    num_of_elements = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title