import os
import random
import re
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals, F
from django.dispatch import receiver
from django.utils import timezone

from .model_validators import validate_file_extension_posts_media


def upload_posts_media_to(instance, filename):
    username = instance.post.user.username
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f'posts/{username}/{filename}'


class PostManager(models.Manager):
    def share(self, user, post, quote_text=None):
        shared_post_parent = None

        if post.parent:
            shared_post_parent = post.parent
        if post.shared_post:
            post = post.shared_post
        shared_post = self.get_queryset().filter(
            user=user, parent=shared_post_parent
        ).filter(
            created__year=timezone.now().year,
            created__month=timezone.now().month,
            created__day=timezone.now().day,
            shared_post__isnull=False,
        )
        if shared_post.exists():
            shared_post.delete()
            return None

        share_post = self.model(
            parent=shared_post_parent,
            user=user,
            text=quote_text,
            shared_post=post,
        )
        share_post.save()

        return share_post

    def like(self, user, post):
        if user in post.likes.all():
            is_liked = False
            post.likes.remove(user)
        else:
            is_liked = True
            post.likes.add(user)
        return is_liked


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
    text = models.CharField(max_length=500, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    shared_post = models.ForeignKey('self', blank=True, null=True,
                                    verbose_name='If shared only',
                                    related_name='post_shared')

    objects = PostManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.id} : {self.user}'

    def create_post(self, user, text):
        self._create(user=user, text=text)

    def create_reply(self, user, text, parent):
        self._create(user=user, text=text, parent=parent)

    def _create(self, user, text, parent=None):
        self.objects.create(user=user, text=text, parent=parent)

    def get_parent(self):
        x = self.parent if self.parent else None
        return x

    def get_childs(self):
        childs = Post.objects.filter(parent=self)
        return childs if childs.exists() else None

    def get_medias(self):
        return self.posts_media.all() if self.posts_media.exists() else None

    def fullName(self):
        # Any expensive calculation on instance data
        # This returning value is cached and not calculated again
        return self.user.first_name + " " + self.user.last_name


class Tag(models.Model):
    tag = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'#{self.tag}'


@receiver(signals.post_save, sender=Post)
def create_tags(sender, instance, created, *args, **kwargs):
    if created:
        tag_regex = r'#(?P<tag>[\w\d-]+)'
        if instance.text:
            tags = re.findall(tag_regex, instance.text)
            for tag in tags:
                _tag = Tag.objects.filter(tag__iexact=tag)
                if _tag.exists():
                    _tag.update(count=F('count') + 1)
                else:
                    Tag.objects.create(tag=tag)


@receiver(signals.post_save, sender=Post)
def create_metadata_for_post(sender, instance, created, **kwargs):
    if created:
        PostsMetadata.objects.create(post=instance)
