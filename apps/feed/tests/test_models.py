from django.contrib.auth import get_user_model
from django.test import TestCase

from feed.models import Feed
from posts.models import Post


class FeedModelTest(TestCase):
    """Tests for feed creation when `Post` is saved."""

    def setUp(self):
        """Create some users and posts for testing."""
        # Create few users first
        self.user = get_user_model().objects.create_user(
            username='test_user1',
            email='test@mail.com',
            password='hlo',
        )

        self.user2 = get_user_model().objects.create_user(
            username='test_user2',
            email='test2@mail.com',
            password='hloo',
        )

        self.user3 = get_user_model().objects.create_user(
            username='test_user3',
            email='test3@mail.com',
            password='hlooo',
        )

        # follow user
        self.user2.user_details.follows.add(self.user.user_details)
        self.user3.user_details.follows.add(self.user.user_details)

        # create few posts with post, replies, shared_posts, and post with mentions
        self.post = Post.objects.create(text='thisistesting', user=self.user)
        self.post_reply = Post.objects.create(
            text='replyplease', user=self.user2, parent=self.post)
        self.post_shared = Post.objects.share(
            quote_text='hlo', user=self.user2, post=self.post)
        self.post_with_mention = Post.objects.create(
            text=f'hi @{self.user.username} hi', user=self.user3)

    def test_own_post_show_up_on_feed(self):
        """Test if own posts are shown up in the feed."""
        self.assertTrue(Feed.objects.filter(
            post=self.post, user=self.user).exists())
        self.assertTrue(Feed.objects.filter(
            post=self.post_reply, user=self.user2).exists())
        self.assertTrue(Feed.objects.filter(
            post=self.post_shared, user=self.user2).exists())
        self.assertTrue(Feed.objects.filter(
            post=self.post_with_mention, user=self.user3).exists())

    def test_post_shown_on_following_users_feed(self):
        """Test if posts are shown to the following users."""
        self.assertTrue(Feed.objects.filter(
            post=self.post, user=self.user2).exists())
        self.assertTrue(Feed.objects.filter(
            post=self.post, user=self.user3).exists())

    def test_post_replies_by_others_are_shown_to_the_original_post_author_feed(self):
        """Test if replies on user's post are shown up in the feed."""
        self.assertTrue(Feed.objects.filter(
            post=self.post_reply, user=self.user).exists())

    def test_post_replies_on_posts_to_user_following_authors_post(self):
        """Test if replies to the post are shown to the user follwing."""
        self.assertTrue(Feed.objects.filter(
            post=self.post_reply, user=self.user3).exists())

    def test_post_shared_are_shown_in_original_post_author_feed(self):
        """Test if shared_posts are shown up in the original post author."""
        self.assertTrue(Feed.objects.filter(
            post=self.post_shared, user=self.user).exists())

    def test_post_mention_with_user_show_up_in_users_feed(self):
        """Test if posts with user mentioned show up in the user's feed."""
        self.assertTrue(Feed.objects.filter(
            post=self.post_with_mention, user=self.user).exists())

    def test_post_mention_with_user_show_up_in_followings_of_friends_feed(self):
        """Test if posts with mention are shown up to the user following."""
        self.assertTrue(Feed.objects.filter(
            post=self.post_with_mention, user=self.user2).exists())
