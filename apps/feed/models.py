from django.db import models

from django.db.models import signals
from django.dispatch import receiver

from django.contrib.auth.models import User

from posts.models import Post

class Feed(models.Model):
    post = models.ForeignKey(Post)
    updated_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="feed")


@receiver(signals.post_save, sender=Post)
def create_feed_for_following_users(sender, instance, created, **kwargs):
    if created:
        Feed.objects.create(
            post=instance, user=instance.user
            )
        for user_details in instance.user.user_details.followed_by.all():
            feed_post = Feed.objects.create(post=instance, user=user_details.user)
