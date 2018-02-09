from django.shortcuts import render, reverse, redirect
from .forms import PostForm, PostMediaFormSet


def posts_add(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        media_form_set = PostMediaFormSet(request.POST, request.FILES)
        if post_form.is_valid() and media_form_set.is_valid():
            post = post_form.save(request.user)
            media_form_set.save(post)
            return redirect(reverse('Home'))
    elif request.method == 'GET':
        post_form = PostForm()
        media_form_set = PostMediaFormSet()

    return render(request, 'posts/post_add.html', {
            'mediaformset': media_form_set,
            'post_form': post_form,
            })
