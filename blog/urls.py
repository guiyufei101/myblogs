from django.urls import path
from . import views
#http://localhost:8000/blog/1
#http://localhost:8000
#以blog开头的
urlpatterns=[
    path('',views.blog_list,name='blog_list'),#定义了博客列表的链接了
    #http://127.0.0.1:8000/blog/1
    path('<int:blog_pk>',views.blog_detail,name="blog_detail"),
    path('',views.search,name='search'),
    #类型的一个连接<>内为类型的一个主键
    path('type/<int:blogs_type_pk>',views.blogs_with_type,name="blogs_with_type"),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name="blogs_with_date"),


]