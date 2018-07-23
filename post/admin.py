from django.contrib import admin
from .models import Post,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','comment','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ['title','body']
    raw_id_fields = ['author',]
    date_hierarchy = 'publish'
    ordering = ['status','publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','post','email','created','updated','active']
    list_filter = ['active','created']
    search_fields = ['name','post']
    ordering = ['created']
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
