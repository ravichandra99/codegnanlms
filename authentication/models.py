from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify


class MyUser(AbstractUser):
    college = models.CharField(max_length = 100)
    branch = models.CharField(max_length = 100)
    mobile = PhoneNumberField()
    display_pic = models.ImageField(upload_to = '', default = 'python.jpg')
    slug = models.SlugField(default = '')


    class Meta:
        verbose_name = "Codegnan User"
        verbose_name_plural = "Codegnan Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(MyUser, self).save(*args, **kwargs)

    