import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F
from django.http import JsonResponse
from django.views.generic import TemplateView

from posts.forms import PostForm, PostMediaFormSet
from posts.models import Post

from .models import Feed
from .serializers import FeedSerializer


class landing_view(TemplateView):
    template_name = 'landing.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mediaformset'] = PostMediaFormSet()
        context['post_form'] = PostForm()
        return context


@login_required
def retrieve_new_post(request, post_id):
    created_on = Post.objects.filter(
        pk=post_id
    ).values_list(
        'created',
        flat=True
    )
    new_feed = Post.objects.filter(
        feed__user=request.user
    ).order_by('-created').filter(created__gt=created_on).annotate(post_user=F('user__username'),
                                                                   userfname=F(
                                                                       'user__first_name'),
                                                                   like_count=Count(
                                                                       'likes'),
                                                                   userlname=F(
                                                                       'user__last_name')
                                                                   ).values()[:100]

    serialized_response = json.dumps(list(new_feed), cls=DjangoJSONEncoder)
    return JsonResponse(serialized_response, safe=False)


@login_required
def get_feed_lists(request):
    feed = Feed.objects.filter(user=request.user).order_by('-updated_on')[:100]
    print(feed)
    serialized_data = FeedSerializer(feed, context={'request': request}, many=True).data
    return JsonResponse(serialized_data, safe=False)


def get_recent_after(request, post_id):
    created_on = Feed.objects.filter(
        post_id=post_id,
        user=request.user,
    ).values_list(
        'updated_on',
        flat=True
    )
    new_feed = Feed.objects.filter(
        user=request.user
        ).filter(
            updated_on__gt=created_on[0]
            ).order_by('-updated_on')[:100]

    serialized_data = FeedSerializer(new_feed, context={'request': request}, many=True).data
    return JsonResponse(serialized_data, safe=False)


def get_posts_before(request, post_id):
    created_on = Feed.objects.filter(
        post_id=post_id,
        user=request.user,
    ).values_list(
        'updated_on',
        flat=True
    )
    new_feed = Feed.objects.filter(
        user=request.user
        ).filter(
            updated_on__lt=created_on[0]
            ).order_by('-updated_on')[:100]

    serialized_data = FeedSerializer(new_feed, context={'request': request}, many=True).data
    return JsonResponse(serialized_data, safe=False)