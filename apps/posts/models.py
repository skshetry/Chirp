import uuid
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    user = models.ForeignKey(User)
    # media = models.ManyToManyField(Media, blank=True, null=True)
    text = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_retweet = models.BooleanField(default=False)
    # metadata = models.OneToOneField()
