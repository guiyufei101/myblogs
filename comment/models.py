from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # ContentType为对应的模型
    object_id = models.PositiveIntegerField()  # 对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上述两个


    text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    #记录每个评论的顶级
    root=models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
    #他的上一级 记录他的上一级可知道他回复的是哪个评论的
    #parent_id=models.IntegerField(default=0)
    parent=models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)
    #回复谁哪个人
    reply_to=models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.text
    class Meta:
        ordering=['comment_time']

#回复

