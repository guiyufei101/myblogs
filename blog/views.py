from django.shortcuts import render,render_to_response,render,get_object_or_404#可能获取不到博客
from .models import BlogType,Blog,ReadNum
from django.core.paginator import Paginator
import datetime
from read_statistics.models import ReadNum,ReadDetail
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from likes.models import LikeRecord,LikeCount
from mysite.forms import LoginForm
# Create your views here.
def blog_list(request):
    context={}
    blogs_all_list=Blog.objects.all()
    page_num=request.GET.get('page',1)#获取url页面参数get请求
    paginator=Paginator(blogs_all_list,5)#每5篇进行分页
    page_of_blogs=paginator.get_page(page_num)#得到页码所对应的页面
    context['page_of_blogs']=page_of_blogs
    #获取当前页
    current_page_num=page_of_blogs.number
    #显示当前页码左右共5页
    #判断当前页和1页找出最大的一直到当前页
    #判断当前页加上2和最大的页找出他们的小值，从当前到小值正好弄了5页
    page_range=list(range(max(1,current_page_num-2),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))

    if page_range[0] -1 >=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1] >=2:
        page_range.append('...')
    if page_range[0] !=1:
        page_range.insert(0,1)#如果显示的第一页不是首页就加入首页
    if page_range[-1] !=paginator.num_pages:#如果不是最后一页
        page_range.append(paginator.num_pages)
    context['page_range']=page_range
    context["blogs"]=Blog.objects.all()
    #一共页
    context['num_pages']=paginator.num_pages
    context['current_page']=current_page_num
    #获取博客的数量
    #context["blog_types"]=BlogType.objects.all()
    types=BlogType.objects.all()
    for blog_type in types:#类对应的可以将数量放到博客类型里面
       blog_type.blogcount= Blog.objects.filter(type=blog_type).count()
    context["blogs_count"]=Blog.objects.all().count()
    context["blog_types"]=types
    dates=Blog.objects.dates('created_time','month',order="DESC")#降序
    #获取日期归档对应的数量
    blog_dates_dict={}
    for blog_date in dates:#取出日期 不像类可以直接相加
        blog_count=Blog.objects.filter(created_time__year=blog_date.year,
                            created_time__month=blog_date.month).count()#进行筛选
        blog_dates_dict[blog_date]=blog_count
    context["blog_dates"]=blog_dates_dict
    count=Blog.objects.all().count()
    counts=count-4
    #latest_blogs=Blog.objects.order_by('created_time')[counts:]两种都行  下边的简单
    latest_blogs=Blog.objects.order_by('-created_time')[:4]

    ct = ContentType.objects.get_for_model(Blog)
    #blog_comments=ReadNum.objects.filter(contenttype=ct).order_by('read_num')[:5]
    blog_comments=Blog.objects.order_by('read_details')[:5]
    context['latest_blogs']=latest_blogs
    context['blog_comments']=blog_comments
    return render(request,'blog_list.html',context)
from django.db.models import Q
def search(request):
    query=request.GET.get('query')
    error_message=''
    if not query:
        error_message='输入关键词'
        return render(request,'home.html',{'error_message':error_message})
    blog_list=Blog.objects.filter(Q(title__icontains=query) | Q(text__icontains= query))
    return render(request,'blog_detail.html',{'error_message':error_message,'blog_list':blog_list})
def blog_detail(request,blog_pk):
    context={}
    blog=get_object_or_404(Blog,pk=blog_pk)
    '''if not request.COOKIES.get('blog_%s_readed' % blog_pk):#不存在这个键值时进行加1操作
    #这个字段取到了  那么阅读计数加1
        if ReadNum.objects.filter(blog=blog).count():
            #存在记录
            readnum=ReadNum.objects.get(blog=blog)#存在这条博客
            readnum.read_num += 1
            readnum.save()
        else:
            #不存在对应记录
            readnum=ReadNum()
            readnum.read_num =1
            readnum.blog=blog#给博客赋值
            readnum.save()
        #blog.readed_num+=1
        #blog.save()
    '''
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):  # 不存在这个键值时进行加1操作
        # 这个字段取到了  那么阅读计数加1
        ct=ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type=ct,object_id=blog.pk).count():
            readnum=ReadNum.objects.get(content_type=ct,object_id=blog.pk)
            readnum.read_num += 1
            readnum.save()
        else:
            readnum=ReadNum(content_type=ct,object_id=blog.pk)
            # 存在记录
            #readnum = ReadNum.objects.get(blog=blog)  # 存在这条博客
            readnum.read_num = 1
            readnum.blog=blog
            readnum.save()

    context["blog"]=blog
    blog_content_type=ContentType.objects.get_for_model(blog)
    data={}
    #获取类的模型在这是blog模型
    data['content_type']=blog_content_type.model
    #获取博客的id
    data['object_id']=blog_pk
    context['comment_form']=CommentForm(initial=data)#实例化传到前端
    #取到博客的评论内容
    blog_content_type=ContentType.objects.get_for_model(blog)
    #获取评论顶级第一条评论
    comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    context['comments']=comments
    #initial初始化 顶级评论的父为0
    context['comment_form']=CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk,'reply_commet_id':0})
    #获取上一条博客
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    #获取下一条博客
    #context['user']=request.user#得到用户
    context['login_form']=LoginForm()
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()
    #=render_to_response('blog_detail.html',context)#响应

    response = render(request,'blog_detail.html', context)  # 响应
    response.set_cookie('blog_%s_readed' % blog_pk,'true',max_age=60,expires=datetime)#将数据保存起来60s内有效
    return response



def blogs_with_type(request,blogs_type_pk):
    context={}
    #找出博客类型系列
    blog_type = get_object_or_404(BlogType, pk=blogs_type_pk)
    blogs=Blog.objects.filter(type=blog_type)
    page_num=request.GET.get('page',1)
    paginator=Paginator(blogs,5)
    page_of_blogs=paginator.get_page(page_num)
    context['page_of_blogs']=page_of_blogs
    # 获取当前页
    current_page_num = page_of_blogs.number
    # 显示当前页码左右共5页
    # 判断当前页和1页找出最大的一直到当前页
    # 判断当前页加上2和最大的页找出他们的小值，从当前到小值正好弄了5页
    page_range = list(range(max(1, current_page_num - 2), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)  # 如果显示的第一页不是首页就加入首页
    if page_range[-1] != paginator.num_pages:  # 如果不是最后一页
        page_range.append(paginator.num_pages)
    context['page_range'] = page_range
    # 一共页
    context['num_pages'] = paginator.num_pages
    context['current_page'] = current_page_num
    #找出每种类型的博客有多少篇
    context['blogs']=blogs
    context['blogs_count']=Blog.objects.filter(type=blog_type).count()
    context['blog_type']=blog_type
    return render(request,'blogs_with_type.html',context)
def blogs_with_date(request,year,month):
    context={}
    #找出博客系列

    #blog_dates=get_object_or_404(Blog,year=)
    blogs=Blog.objects.filter(created_time__year=year,created_time__month=month)#获取所取__年月的博客
    context["blogs_count"]=blogs.count()

    context["blogs_with_date"]='%s年%s月' %(year,month)
    context["blogs"]=blogs
    context["blog_dates"] = Blog.objects.dates('created_time', 'month', order="DESC")  # 降序
    return render(request,'blogs_with_date.html',context)
