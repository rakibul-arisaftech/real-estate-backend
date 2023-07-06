import os
from django.db import models
from django.conf import settings
from .managers import CustomUserManager
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from property.models import Property

def no_special_char(value): 
    if '@' in value or '!' in value or '#' in value or '$' in value or '%' in value or '^' in value or '&' in value or '*' in value or '+' in value or '-' in value or '.' in value:
        raise ValidationError("This field is not accept special character or space..")

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=80,
        unique=True,
        validators=[no_special_char],
    )
    email = models.EmailField(unique=True)
    # change_email = models.EmailField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

            
    def __str__(self):
        return f'{self.username}'


def get_image_filename(instance, filename):
    name = instance.first_name
    slug = slugify(name)
    return f"images/profile/{slug}-{filename}"


class Wishlist(models.Model):
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

    def __str__(self):
        return self.user.email

    @property
    def filename(self):
        return os.path.basename(self.image.name)