from django.db import models
from django.forms import ModelForm


# Create your models here.
class Images(models.Model):
    file = models.ImageField(upload_to='profile_photos')


class ImageUploadForm(ModelForm):
    class Meta:
        model = Images
        fields = ['file']
