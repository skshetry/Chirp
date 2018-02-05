from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import random


def upload_posts_media_to(instance, filename):
    username = instance.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'photos/{username}/{filename}'


class User_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(max_length=300, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    follows = models.ManyToManyField('User_details', related_name='followed_by')
    profile_photo = models.ImageField(null=True, upload_to=upload_posts_media_to, default=None)
    cover_photo = models.ImageField(null=True, upload_to=upload_posts_media_to, default=None)

    @property
    def cover_photo_url(self):
        if self.cover_photo and hasattr(self.cover_photo, 'url'):
            return self.cover_photo.url


    @property
    def profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_details.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_details.save()
