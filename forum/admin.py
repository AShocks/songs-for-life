from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Customise the admin panel, use summernote for the forum content
    """
    list_display = ('title', 'author', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    actions = ['approve_posts']

    def approve_post(self, request, queryset):
        """
        Method to approve posts
        """
        queryset.update(appoved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Manage the comment section
    """
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """
        Method to approve comments
        """
        queryset.update(approved=True)
