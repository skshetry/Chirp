from django.conf.urls import url

from apps.search import views as search_views

urlpatterns = [
    # For autocomplete suggestions
    # url(r'^autocomplete/$', search_views.get_autocomplete_suggestions, name='autocomplete'),
    url(r'^search/$', search_views.search, name='search'),
]
