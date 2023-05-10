from django.db import models

# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/service/')

    def __str__(self):
        return self.title


    
class Category(models.Model):
    title = models.CharField(max_length=254)
    num = models.IntegerField()
    image = models.ImageField(upload_to='images/category/')

    def __str__(self):
        return self.title
    
class Property(models.Model):
    title = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    rooms = models.IntegerField()
    baths = models.IntegerField()
    price = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/property/')

    def __str__(self):
        return self.title
    

