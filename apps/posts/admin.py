from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, PostMedia, PostsMetadata, Tag


class PostMediaAdminInline(admin.StackedInline):
    model = PostMedia
    readonly_fields = ('image_img', 'media', 'media_type')

    def image_img(self, obj):
        return mark_safe(f'<img src="{obj.media.url}" width="{obj.media.width}" height="{obj.media.height}"')

    def has_add_permission(self, request, obj=None):
        return False


class PostsMetadataAdminInline(admin.StackedInline):
    model = PostsMetadata
    readonly_fields = ('views', 'impressions')

    def has_change_permission(self, request, obj=None):
        return False


class PostAdmin(admin.ModelAdmin):
    inlines = [PostMediaAdminInline, PostsMetadataAdminInline]
    list_display = ('id', 'user', 'text', 'is_shared', 'is_reply', 'created')
    readonly_fields = ('id', 'user', 'text', 'is_shared', 'is_reply', 'likes', 'shared_post', 'parent')
    list_filter = ('user',)
    search_fields = ('text', 'id', 'user__username')
    list_per_page = 100
    ordering = ('-created', 'id', 'user')

    def is_reply(self, obj):
        return True if obj.parent else False

    def is_shared(self, obj):
        return True if obj.shared_post else False

    def has_add_permission(self, request):
        return False

    is_reply.boolean = True
    is_shared.boolean = True


admin.site.register(Post, admin_class=PostAdmin)
admin.site.register(Tag)
admin.site.register(PostsMetadata)
admin.site.register(PostMedia)
