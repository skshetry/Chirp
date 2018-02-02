import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from posts.models import Post
from .decorators import ajax_required
# Create your views here.

def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        try:
            search_type = request.GET.get('type')
            if search_type not in ['posts', 'users']:
                search_type = 'posts'
        except Exception:
            search_type = 'posts'
        
        count = {}
        results = {}
        results['posts'] = Post.objects.filter(text__icontains=querystring, parent=None)
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) | Q(
                    last_name__icontains=querystring))
        count['posts'] = results['posts'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],        
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})

