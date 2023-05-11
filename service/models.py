from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/service/')

    def __str__(self):
        return self.title