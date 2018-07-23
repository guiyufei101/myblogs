from django.contrib import admin
from .models import LikeRecord,LikeCount
# Register your models here.

class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['id','liked_num','content_object']


admin.site.register(LikeCount,LikeCountAdmin)

