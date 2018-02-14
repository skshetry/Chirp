from django.shortcuts import render
from django.views.generic import TemplateView

from django.core import serializers
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from posts.forms import PostMediaFormSet, PostForm
from posts.models import Post
from django.db.models import F 

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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
        ).order_by('-created').filter(created__gt=created_on).annotate(postuser=F('user__username'))[:100]
    serialized_response = serializers.serialize('json', new_feed)
    return JsonResponse(serialized_response, safe=False)