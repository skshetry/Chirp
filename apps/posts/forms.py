from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ValidationError

from .models import Post, PostMedia


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'shared_post']

    def save(self, user, shared_post_id=None, parent_id=None,commit=True, *args, **kwargs):
        instance = super().save(commit=False,)
        instance.user = user
        if shared_post_id:
            post = Post.objects.get(pk=shared_post_id)
            if post.shared_post:
                    instance.shared_post = post.shared_post
                    instance.parent = post.shared_post.parent
            else:
                instance.shared_post = post
                instance.parent = post.parent
        if parent_id:
            post = Post.objects.get(pk=parent_id)
            if post:
                instance.parent = post
        if commit:
            instance.save()
        return instance

    def clean(self,*args,**kwargs):
        super().clean(*args,**kwargs)
        if len(self.cleaned_data.get('text')) > 140:
            raise ValidationError("Character limit exceeded. Posts should be less than 140 characters.")


class BasePostMediaFormSet(BaseModelFormSet):
    def save(self, post, commit=True):
        instances = super().save(commit=False)
        for instance in instances:
            instance.post = post
            if commit:
                instance.save()
        return instances


PostMediaFormSet = modelformset_factory(
    PostMedia,
    fields=('media',),
    extra=0,
    formset=BasePostMediaFormSet
    )
