from django.db import models
from django.conf import settings

# Create your models here.
class Service(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="service",
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/service/')

    def __str__(self):
        return self.title