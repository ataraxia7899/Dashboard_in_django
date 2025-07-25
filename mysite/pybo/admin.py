from django.contrib import admin
from .models import User, Post, Comment, PostLike, Bookmark

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'content', 'user__username')

# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(Bookmark)
