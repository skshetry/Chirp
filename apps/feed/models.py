import itertools

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
        users = itertools.chain(User.objects.filter(pk=instance.user.id).values_list('pk', flat=True))
        users = itertools.chain(users, instance.user.user_details.followed_by.all() \
                                             .values_list('user__id',
                                                          flat=True)
        )

        # show replies on your own post
        if instance.parent:
            users = itertools.chain(users, User.objects.filter(pk=instance.parent.user.id).values_list('pk', flat=True))
            users = itertools.chain(users, instance.parent.user.user_details.followed_by.all() \
                                                         .values_list('user__id',
                                                                      flat=True)
            )

        # show your post shared in feed
        if instance.shared_post:
            users = itertools.chain(users, User.objects.filter(pk=instance.shared_post.user.id).values_list('pk', flat=True))

        # if mentioned show that post to all
        import re
        mention_regex = r'@(?P<tag>[\w\d-]+)'
        if instance.text:
            mentions = re.findall(mention_regex, instance.text)
            for mention in mentions:
                _user = User.objects.filter(username__iexact=mention)
                if _user.exists():
                    users = itertools.chain(users, User.objects.filter(pk=_user.get().id).values_list('pk', flat=True))
                    users = itertools.chain(users, _user.get().user_details.followed_by.all() \
                                                        .values_list('user__id',
                                                                     flat=True)
                    )

        feed = [Feed(post=instance,
                     user=User.objects.get(pk=user)
                     ) for user in set(users)]

        Feed.objects.bulk_create(feed)
