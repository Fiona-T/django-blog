from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # to populate the slug field from the title field
    prepopulated_fields = {'slug': ('title',)}
    # add filter box to filter by status or by created date
    list_filter = ('status', 'created_on')
    # to change the default list display (__str__) to selected fields
    list_display = ('title', 'slug', 'status', 'created_on')
    # add search box allowing search on title field and content field
    search_fields = ['title', 'content']
    # to add wysiwyg editor to the content field
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    # add approve_comments to appear in actions drop down
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
