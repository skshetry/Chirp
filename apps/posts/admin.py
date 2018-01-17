from django.contrib import admin

from .models import Post, PostMedia, PostsMetadata, Tag


class PostMediaAdminInline(admin.StackedInline):
    model = PostMedia


class PostsMetadataAdminInline(admin.StackedInline):
    model = PostsMetadata

    def has_change_permission(self, request, obj=None):
        return False


class PostAdmin(admin.ModelAdmin):
    inlines = [PostMediaAdminInline, PostsMetadataAdminInline]


admin.site.register(Post, admin_class=PostAdmin)
admin.site.register(Tag)
admin.site.register(PostsMetadata)
