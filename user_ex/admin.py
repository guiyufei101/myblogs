from django.contrib import admin
from .models import Profile,User_Avatar
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
class UserAdmin(BaseUserAdmin):
    inlines=(ProfileInline,)
    list_display=['username','nickname','avatar','email','is_staff','is_active','is_superuser']

    def nickname(self,obj):
        return obj.profile.nickname
    nickname.short_description ='昵称'

    def avatar(self,obj):
        return obj.user_avatar.avatar
    avatar.short_description='图片'
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','nickname']

class User_AvatarAdmin(admin.ModelAdmin):
    list_display = ['user','avatar']
admin.site.register(Profile,ProfileAdmin)
admin.site.register(User_Avatar,User_AvatarAdmin)

