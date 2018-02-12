from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.forms import PostMediaFormSet, PostForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'feed/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mediaformset'] = PostMediaFormSet()
        context['post_form'] = PostForm()
        return context

