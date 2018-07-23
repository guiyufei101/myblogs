from django.contrib import admin
from .models import Blog,BlogType,ReadNum,User
# Register your models here.
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','type','author','get_read_num','created_time','last_updated_time']
    search_fields = ['title','type','author']
    list_per_page = 5#每页显示博客数目
    list_display_links = ['title','author']#链接可以点击进去的列
    list_filter = ['created_time']#根据类型进行过滤
admin.site.register(BlogType, BlogTypeAdmin)
admin.site.register(Blog, BlogAdmin)

'''class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num','blog']


admin.site.register(ReadNum,ReadNumAdmin)
'''