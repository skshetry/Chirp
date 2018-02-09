from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, ValidationError
from .models import Post, PostMedia


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text',]

    def save(self, user, commit=True, *args, **kwargs):
        instance = super().save(commit=False,)
        instance.user = user
        if commit:
            instance.save()
        return instance

    def clean(self,*args,**kwargs):
        super().clean(*args,**kwargs)
        if len(self.cleaned_data.get('text')) > 140:
            raise ValidationError("Character limit exceeded.")


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
