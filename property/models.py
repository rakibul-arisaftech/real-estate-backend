from django.db import models

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=60)
    size = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    rooms = models.PositiveIntegerField(default=0)
    baths = models.PositiveIntegerField(default=0)
    price = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/property/')

    def __str__(self):
        return self.title