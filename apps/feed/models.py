from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from posts.models import Post


class Feed(models.Model):
    post = models.ForeignKey(Post)
    updated_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="feed")


@receiver(signals.post_save, sender=Post)
def create_feed_for_following_users(sender, instance, created, **kwargs):
    if created:
        # show my own posts
        Feed.objects.create(
            post=instance, user=instance.user
        )

        # show post to all users that follow
        for user_details in instance.user.user_details.followed_by.all():
            Feed.objects.create(post=instance, user=user_details.user)

        # show your post shared in feed
        if instance.shared_post:
            Feed.objects.create(
                post=instance, user=instance.shared_post.user
            )
        # show replies on your own post
        if instance.parent:
            Feed.objects.create(
                post=instance, user=instance.parent.user,
            )
            # show replies to all users
            for user_details in instance.parent.user.user_details.followed_by.all():
                Feed.objects.create(
                    post=instance, user=user_details.user,
                )

        # if mentioned show that post to all
        import re
        mention_regex = r'@(?P<tag>[\w\d-]+)'
        if instance.text:
            mentions = re.findall(mention_regex, instance.text)
            for mention in mentions:
                _user = User.objects.filter(username__iexact=mention)
                if _user.exists():
                    # show up to the user's post if mentioned
                    Feed.objects.create(
                        post=instance, user=_user.first(),
                    )
                    # show to all users that are following the user mentioned in the post
                    for user_details in _user.get().user_details.followed_by.all():
                        Feed.objects.create(
                            post=instance, user=user_details.user,
                        )
