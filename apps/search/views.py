from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.db.models import (BooleanField, Case, Count, IntegerField, Q,
                              Value, When)
from django.shortcuts import redirect, render

from feed.templatetags.post_include import get_all_posts
from posts.forms import PostForm, PostMediaFormSet
from posts.models import Post


@login_required
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
        results = {'posts': Post.objects.none()}
        queries = querystring.split()
        for query in queries:
            results['posts'] = results['posts'] | get_all_posts().filter(
                text__icontains=query)
            results['users'] = User.objects.filter(
                Q(username__icontains=query) | Q(
                    first_name__icontains=query) | Q(
                        last_name__icontains=query))

        # full text search
        query = SearchQuery(querystring)
        vector = SearchVector('text')

        result_fulltext = get_all_posts().annotate(
            post_liked=Case(
                When(likes=request.user, then=True),
                default=Value(False),
                output_field=BooleanField(),
            )).annotate(
            shared=Case(
                When(post_shared__user=request.user, then=True),
                When(shared_post__user=request.user, then=True),
                default=Value(False),
                output_field=BooleanField(),
            )).annotate(
            shared_count=Case(
                When(shared_post__isnull=True,
                     then=Count('post_shared')),
                output_field=IntegerField(),
            )).annotate(
            rank=SearchRank(vector, query)
        ).filter(rank__gte=0.0001).order_by('-rank')

        results['posts'] = result_fulltext | results['posts']

        count['posts'] = results['posts'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
            'mediaformset': PostMediaFormSet(),
            'post_form': PostForm(),
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})
