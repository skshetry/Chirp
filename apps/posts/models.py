import os
import random
import re
import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from django.contrib.auth.models import User

from .model_validators import validate_file_extension_posts_media


def upload_posts_media_to(instance, filename):
    username = instance.post.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'posts/{username}/{filename}'


class PostMedia(models.Model):
    media = models.FileField(upload_to=upload_posts_media_to, validators=[validate_file_extension_posts_media])
    media_type = models.CharField(default='image', max_length=6)
    post = models.ForeignKey('Post', related_name='posts_media')
    uploaded = models.DateTimeField(auto_now_add=True)


class PostsMetadata(models.Model):
    views = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    post = models.OneToOneField('Post', blank=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='post_childs')
    user = models.ForeignKey(User)
    text = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    shared_post = models.ForeignKey('self', blank=True, null=True, verbose_name='If shared only', related_name='post_shared')

    def __str__(self):
        return f'{self.id} : {self.user}'


class Tag(models.Model):
    tag = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.tag}'


@receiver(signals.post_save, sender=Post)
def create_tags(sender, instance, created, *args, **kwargs):
    if created:
        tag_regex = r'#(?P<tag>[\w\d-]+)'
        tags = re.findall(tag_regex, instance.text)
        for tag in tags:
            Tag.objects.get_or_create(tag=tag)


@receiver(signals.post_save, sender=Post)
def create_metadata_for_post(sender, instance, created, **kwargs):
    if created:
        PostsMetadata.objects.create(post=instance)

