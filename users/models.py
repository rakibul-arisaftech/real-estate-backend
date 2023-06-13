import os
from django.db import models
from django.conf import settings
from .managers import CustomUserManager
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from property.models import Property

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


def get_image_filename(instance, filename):
    name = instance.first_name
    slug = slugify(name)
    return f"images/profile/{slug}-{filename}"


class Wishlist(models.Model):
    # name = models.PositiveIntegerField(_("property_id"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    property = models.ForeignKey(Property, related_name="property", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("wishlist")
        verbose_name_plural = _("wishlists")


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(upload_to=get_image_filename, null=True)
    bio = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    wishlist = models.ManyToManyField(Wishlist, related_name="wishlist", blank=True)
    # wishlist = ArrayField(models.IntegerField(), max_length=10, null=True)

    def __str__(self):
        return self.user.email

    @property
    def filename(self):
        return os.path.basename(self.image.name)

# class Wishlist(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
#     property = models.ForeignKey(Property, related_name="property", on_delete=models.CASCADE)