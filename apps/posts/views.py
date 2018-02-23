from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect

from .forms import PostForm, PostMediaFormSet
from .models import Post


@login_required
def posts_add(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        media_form_set = PostMediaFormSet(request.POST, request.FILES)
        if post_form.is_valid() and media_form_set.is_valid():
            shared_post_id = request.POST.get('shared_post')
            parent_id = request.POST.get('parent')
            if not shared_post_id:
                shared_post_id=None
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
    return JsonResponse({"done": is_liked})


@login_required
def share_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    shared_post = Post.objects.share(user=request.user, post=post)
    is_shared = False
    if shared_post:
        is_shared = True
    return JsonResponse({'done': is_shared})