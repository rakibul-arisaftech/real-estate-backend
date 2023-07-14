from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Property(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="property",
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=60)
    size = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100)
    rooms = models.PositiveIntegerField(default=0)
    baths = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    tag = models.CharField(max_length=5, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/property/')
    property_type = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} by {self.author.username}"



class Comment(models.Model):
    post = models.ForeignKey(Property, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="property_comments",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField(_("Comment body"))
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.author.username}"
