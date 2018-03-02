from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from feed.models import Feed
from posts.models import Post

from .models import User_details


class ProfileInline(admin.StackedInline):
    model = User_details
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ('profile_img', 'cover_img', 'followed_by', 'profile_link', 'followers')

    def profile_link(self, obj):
        link = reverse('user_profile:user_profile', kwargs={'username':obj.username})
        print(obj.username)
        return mark_safe(f'<a href="{link}">View Profile</a>')

    def profile_img(self, obj):
        return mark_safe(f'<img src="{obj.profile_photo.url}" width="{obj.profile_photo.width}" height="{obj.profile_photo.height}"/>')

    def cover_img(self, obj):
        return mark_safe(f'<img src="{obj.cover_photo.url}" width="{obj.cover_photo.width}" height="{obj.cover_photo.height}"/>')

    def followers(self, obj):
        return list(obj.followed_by.all())

class FeedInline(admin.StackedInline):
    model = Feed
    fields = ('post', 'post_text', 'updated_on')
    readonly_fields = ('post', 'post_text', 'updated_on')
    list_display_links = ('feed', 'post')
    list_per_page = 10

    def has_change_permission(self, request, obj=None):
        return True

    def post_text(self, obj=None):
        return obj.post.text

    def has_delete_permission(self, request, obj=None):
        return False

    


class PostInline(admin.StackedInline):
    model = Post
    fields = ('text', 'type_post', 'created')
    readonly_fields = ('text', 'type_post', 'created')

    def type_post(self, obj):
        if obj.shared_post:
            return f'Shared to {obj.shared_post}'
        elif obj.parent:
            return f'Reply to {obj.parent}'
        else:
            return 'Original Post'

    def has_add_permission(self, request, obj=None):
        return False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, FeedInline, PostInline)
    list_display = ('profile_link', 'username', 'email', 'first_name', 'last_name', 'is_staff',)
    def profile_link(self, obj):
        link = reverse('user_profile:user_profile', kwargs={'username':obj.username})
        return f'<a href="{link}">View Profile</a>'
    profile_link.allow_tags = True

    list_display_links = ('username',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
