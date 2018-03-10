import os
import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def upload_posts_media_to(instance, filename):
    username = instance.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'photos/{username}/{filename}'


class UserProfileManager(models.Manager):
    use_for_related_field = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile = User_details.objects.get(user=user)
        if to_toggle_user in user_profile.follows.all():
            user_profile.follows.remove(to_toggle_user)
            added = False
        else:
            user_profile.follows.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = User_details.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class User_details(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_details')
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(max_length=300, null=True)
    GENDER_CHOICES = (
        (None, None),
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    follows = models.ManyToManyField(
        'User_details', related_name='followed_by', blank=True)
    profile_photo = models.ImageField(
        null=True, upload_to=upload_posts_media_to, default=None)
    cover_photo = models.ImageField(
        null=True, upload_to=upload_posts_media_to, default=None)
    objects = UserProfileManager()

    @property
    def cover_photo_url(self):
        if self.cover_photo and hasattr(self.cover_photo, 'url'):
            return self.cover_photo.url

    @property
    def profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_details.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_details.save()
