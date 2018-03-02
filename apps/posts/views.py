from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse

from feed.templatetags import post_include

from .forms import PostForm, PostMediaFormSet
from .models import Post, PostMedia
from .serializers import PostSerializer


@login_required
def posts_add(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        media_form_set = PostMediaFormSet(request.POST, request.FILES)
        if post_form.is_valid() and media_form_set.is_valid():
            shared_post_id = request.POST.get('shared_post')
            parent_id = request.POST.get('parent')
            if not shared_post_id:
                shared_post_id = None
            if not parent_id:
                parent_id = None
            post = post_form.save(request.user, shared_post_id, parent_id)
            media_form_set.save(post)
            return redirect(reverse('feeds:home'))
    elif request.method == 'GET':
        post_form = PostForm()
        media_form_set = PostMediaFormSet()

    return render(request, 'posts/post_add.html', {
        'mediaformset': media_form_set,
        'post_form': post_form,
    })


@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    is_liked = Post.objects.like(request.user, post)
    likes_count = post.likes.count()
    return JsonResponse({"done": is_liked, 'likes_count': likes_count})


@login_required
def share_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    shared_post = Post.objects.share(user=request.user, post=post)
    is_shared = False
    if shared_post:
        is_shared = True
    shares_count = post.post_shared.count()
    return JsonResponse({'done': is_shared, 'shares_count': shares_count})


@login_required
def post_detail(request, post_id):
    post = post_include.get_all_posts().get(pk=post_id)
    print(PostSerializer())
    serialized_data = PostSerializer(post, context={'request': request}).data
    return JsonResponse(serialized_data, safe=False)


@login_required
def get_media(request, media_id):
    media = PostMedia.objects.get(pk=media_id)
    return redirect(media.media.url)
