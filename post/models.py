from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

#评论
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['-created',]
    def __str__(self):
        return 'comment by %s on %s'%(self.name,self.post)
