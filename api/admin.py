from django.contrib import admin
from .models import Service, Category, Property

# Register your models here.
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Property)