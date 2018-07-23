from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.
class ReadNum(models.Model):
    read_num=models.IntegerField()
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)#ContentType为对应的模型
    object_id=models.PositiveIntegerField()#对应模型的主键值
    content_object=GenericForeignKey('content_type','object_id')#将上述两个字段统一起来变为一个通用的外键
class ReadDetail(models.Model):
    date=models.DateField(default=timezone.now)
    read_num=models.IntegerField()
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
