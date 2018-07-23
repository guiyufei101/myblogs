from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=30,verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname,self.user.username)

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile=Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''
User.get_nickname=get_nickname
#绑定方法
def has_nickname(self):
    return Profile.objects.filter(user=self).exists()
User.has_nickname=has_nickname

def has_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile=Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username
User.has_nickname_or_username=has_nickname_or_username



from types import MethodType#类的动态绑定方法
import os
# Create your models here.
#头像上传目录
AVATAR_TOOT='static/media/avatar'
AVATAR_DEFAULT='media/upload/05/03/redis.jpg'
class User_Avatar(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to=AVATAR_TOOT)
    def __str__(self):
        return '<Profile: %s for %s>' % (self.avatar,self.user.username)
    #动态绑定头像的方法
    def get_avatar_url(self):
        try:
            avatar=User_Avatar.objects.get(user=self.id)
            return avatar.avatar
        except Exception as e:
            return AVATAR_DEFAULT
#动态绑定方法
#User.get_avatar_url = MethodType(get_avatar_url, None, User)