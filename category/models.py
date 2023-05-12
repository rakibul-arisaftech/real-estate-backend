from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=60)
    num_of_elements = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/category/')

    def __str__(self):
        return self.title