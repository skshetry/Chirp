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
        users = [instance.user.id]
        users_qs = instance.user.user_details.followed_by.all() \
                                             .values_list('user',
                                                          flat=True)

        # show replies on your own post
        if instance.parent:
            users += [instance.parent.user.id]
            users_qs |= instance.parent.user.user_details.followed_by.all() \
                                                         .values_list('user',
                                                                      flat=True)

        # show your post shared in feed
        if instance.shared_post:
            users += [instance.shared_post.user.id]

        # if mentioned show that post to all
        import re
        mention_regex = r'@(?P<tag>[\w\d-]+)'
        if instance.text:
            mentions = re.findall(mention_regex, instance.text)
            for mention in mentions:
                _user = User.objects.filter(username__iexact=mention)
                if _user.exists():
                    users += [_user.get().id]
                    users_qs |= _user.get().user_details.followed_by.all() \
                                                        .values_list('user',
                                                                     flat=True)

        # everytime `list()` is done, it will hit database
        # i wanted it to hit only once. So, this
        users = list(users_qs) + users

        feed = [Feed(post=instance,
                     user=User.objects.get(pk=user)
                     ) for user in set(users)]

        Feed.objects.bulk_create(feed)
