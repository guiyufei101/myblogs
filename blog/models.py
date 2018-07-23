from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField#富文本编辑字段
from  ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions
from read_statistics.models import ReadNum,ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import datetime

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
class BlogType(models.Model):
    type_name = models.CharField(max_length=50, verbose_name='类型')

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,verbose_name='博客类型')
    #content=models.TextField(verbose_name='内容')
    #content=RichTextField()富文本功能
    content=RichTextUploadingField()#可以上传图片功能
    read_details=GenericRelation(ReadDetail)#关联模型
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_updated_time=models.DateTimeField(auto_now=True,verbose_name='最后更新时间')
    '''def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist :#不存在阅读计数 则返回0
            return 0
    '''
    def get_read_num(self):
        try:
            ct=ContentType.objects.get_for_model(self)
            readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    class Meta:
        #排序，倒序
        ordering=['-created_time']

    def __str__(self):
        return self.title

'''class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)  # 阅读计数
    blog=models.OneToOneField(Blog,on_delete=models.DO_NOTHING)#一对一关系
'''