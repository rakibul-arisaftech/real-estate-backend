from django.contrib import admin
from .models import Service, Blog, Category, Property

# Register your models here.
admin.site.register(Service)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Property)