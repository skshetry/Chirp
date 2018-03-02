from rest_framework import serializers

from posts.serializers import PostSerializer

from .models import Feed

class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('post', 'post_link')

    post = PostSerializer(read_only=False)
    post_link = serializers.HyperlinkedRelatedField(
        source='post',
        view_name='posts:post_detail',
        lookup_field='pk',
        many=False,
        read_only=True,
        lookup_url_kwarg='post_id'
    )
