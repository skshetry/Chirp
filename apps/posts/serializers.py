from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework import serializers

from .models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')




class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'text', 'user','parent', 'updated', 'created', 'likes',
            'shared_post', 'likes_count', 'liked', 'shared', 'shared_count',
            'reply_count', 'posts_media', 'post_childs', 'user_profile',
            )

    likes = serializers.HyperlinkedRelatedField(
        view_name='user_profile:user_profile',
        lookup_field='username',
        many=True,
        read_only=True
    )
    user_profile = serializers.HyperlinkedRelatedField(
        view_name='user_profile:user_profile',
        lookup_field='username',
        many=False,
        read_only=True,
        source='user',
    )
    posts_media = serializers.HyperlinkedRelatedField(
        view_name='posts:get_media',
        lookup_field='id',
        many=True,
        read_only=True,
        lookup_url_kwarg='media_id'
    )
    parent = serializers.HyperlinkedRelatedField(
        view_name='posts:post_detail',
        lookup_field='pk',
        many=False,
        read_only=True,
        lookup_url_kwarg='post_id'
    )
    shared_post = serializers.HyperlinkedRelatedField(
        view_name='posts:post_detail',
        lookup_field='pk',
        many=False,
        read_only=True,
        lookup_url_kwarg='post_id'
    )
    post_childs = serializers.HyperlinkedRelatedField(
        view_name='posts:post_detail',
        lookup_field='pk',
        many=True,
        read_only=True,
        lookup_url_kwarg='post_id'
    )

    likes_count = serializers.SerializerMethodField()
    shared_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    user = UserSerializer(many=False, read_only=True)
    liked = serializers.SerializerMethodField()
    shared = serializers.SerializerMethodField()

    def get_reply_count(self, obj):
        return obj.post_childs.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        username = self.context.get('request').user.username
        return obj.likes.filter(username=username).exists()

    def get_shared(self, obj):
        user = self.context.get('request').user
        return obj.post_shared.filter(user=user).exists()

    def get_shared_count(self, obj):
        return obj.post_shared.count()
