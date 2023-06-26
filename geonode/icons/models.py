from django import forms
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.html import mark_safe
import os, base64, datetime, time

def unique_filename(path):
    """
    Enforce unique upload file names.
    Usage:
    class MyModel(models.Model):
        file = ImageField(upload_to=unique_filename("path/to/upload/dir"))
    """
    def funcq(instance, filename):
        image_path = time.strftime(path)
        name, ext = os.path.splitext(filename)
        new_name = name + "-" + str(datetime.datetime.now())
        new_name = '-'.join(new_name.replace('.%s', '').split())
        return os.path.join(image_path, new_name + ext)

    return funcq

class Icon(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    path = models.ImageField(upload_to=unique_filename('icons/%Y/%m/%d'),
                                 validators=[FileExtensionValidator(allowed_extensions=["jpg","png"])],
                                )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at", "name", )

    def __str__(self):
        return self.name
    
    def image_tag(self):
            return mark_safe('<img width="32" src="%s"  />' % (self.path.url))

    image_tag.short_description = 'Image'