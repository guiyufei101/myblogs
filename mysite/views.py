from django.shortcuts import render_to_response,render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import Users
import urllib.request
import json
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_seventdays_hot_data
from django.utils import timezone
from django.db.models import Sum
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import LoginForm,RegForm
from django.urls import reverse
from django.http import JsonResponse
from  shop.models import Product
#获取7天的博客
def get_seventdays_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_details__date__lt=today,read_details__date__gt=date)\
        .values('id','title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')#分组统计
    return blogs[:5]

def getExpress(company,code):
    url='http://www.kuaidi100.com/query?type=%s&postid=%s'%(company,code)
    page=urllib.request.urlopen(url)
    return page.read().decode('utf-8')
def showResult(jsonstr):
    jsonobj=json.loads(jsonstr)
    status=jsonobj.get('status')
    list={}
    if status=='200':
        for x in jsonobj.get('data'):
            list["x.get('time')"]=x.get('context')
    return list


#首页
def home(request):
    context={}
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates,read_nums=get_seven_days_read_data(blog_content_type)
    context['dates']=dates
    context['read_nums']=read_nums
    today_hot_data=get_today_hot_data(blog_content_type)
    yesterday_hot_data=get_yesterday_hot_data(blog_content_type)
    #seventdays_hot_data=get_seventdays_hot_data(blog_content_type)
    context['today_hot_data']=today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['seventdays_hot_blogs']=get_seventdays_hot_blogs
    return render(request,'home.html',context)

#错误页
def error(request):
    return render(request,'error.html')


#登录
def login_for_medal(request):
    if request.method=='POST':
        login_form = LoginForm(request.POST)
        data = {}
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            #验证通过返回成功
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)


def login(request):
    '''username=request.POST.get('username','')
    password=request.POST.get('password','')
    #如何验证登录用户
    user=auth.authenticate(request,username=username,password=password)
    #记录先前从哪个页面跳转过来的
    referer=request.META.get("HTTP_REFERER",'/')
    if user is not None:
        auth.login(request,user)
        #重定向到一个页面
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':'用户名或者密码不正确'})
        '''
    referer = request.META.get("HTTP_REFERER", '/')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
        return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User()
            user.username=username
            user.email=email
            user.password=password
            user.save()
            # 登录用户
            #user = auth.authenticate(username=username, password=password)
            #auth.login(request, user)
            return redirect(request.GET.get('from', reverse('login')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def changepassword(request):
    return render(request,'changepassword.html')
#修改密码操作
def changepassword_action(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        password2=request.POST.get('password2','')
        passwordr=request.POST.get('passwordr','')
        if password2==passwordr:
            #User.objects.get(username=username,password=password)
            user=User.objects.filter(username=username,password=password)
            if user is not None:
                User.objects.filter(username=username,password=password).update(password=password2)
                return HttpResponseRedirect('/login/')
            else:
                return render(request,'changepassword.html',{'message':u'用户名或者密码不正确'})
        else:
            return render(request,'changepassword.html',{'message':u"两次输入的密码不一致！"})

def user_info(request,user_pk):
    context={}
    user=get_object_or_404(User,pk=user_pk)
    context['user']=user
    blogs=Blog.objects.all()
    users=User.objects.all()
    products=Product.objects.all()
    context['users']=users
    context['blogs']=blogs
    context['products']=products
    return render(request,'user_info.html',context)
def user_manage(request):
    users=User.objects.all()
    context={}
    context['users']=users
    return render(request,'user_manage.html',context)
#用户管理
def usermanage_action(request):
    return render(request,'user_detail.html')
def user_detail(request,user_pk):
    context={}
    user=get_object_or_404(User,pk=user_pk)
    context['user']=user
    return render(request,'user_detail.html', context)  # 响应
#登出
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))



def search_post(request):
    if request.method=='POST':
        post_name=request.POST.get('post_name','')
        post_id=request.POST.get('post_id','')
        jsonstr=getExpress(post_name,post_id)
        jsonobj=json.loads(jsonstr)
        status=jsonobj.get('status')
        if status=='200':
            context=jsonobj
        else:
            context='没有快递信息'
        #context['datas']=showResult(jsonstr)
    return render('home.html',context)
'''def register(request):
    context={}
    return render('register.html',context)
def register_action(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        if password == password2:
            try:
                Users.objects.get(username=username)
                return render('register.html',{'message': u'用户名已存在'})
            except Users.DoesNotExist:
                users = Users()
                users.username = username
                users.password = password
                users.email = email
                users.save()
                return HttpResponseRedirect('/login/')
        else:
            return render('register.html',{'message': u"两次密码不一致"})
'''
from io import StringIO
from xlwt import *
#导出用户信息
def export(request):
    user_list=User.objects.all().order_by('-date_joined')
    if user_list:
        #创建工作簿
        ws=Workbook(encoding='utf-8')
        w=ws.add_sheet(u"数据报表第一页")
        w.write(0,0,"id")
        w.write(0,1,u"姓名")
        #w.write(0,2,u"昵称")
        w.write(0,2,u"邮箱")
        w.write(0,3,u"加入时间")
        #写入数据
        excel_row=1
        for user in user_list:
            id=user.id
            name=user.username
            #nickname=user.nic
            email=user.email
            join_time=user.date_joined
            w.write(excel_row,0,id)
            w.write(excel_row, 1, name)
            w.write(excel_row, 2, email)
            w.write(excel_row, 3, join_time)
            excel_row+=1
        ws.save("user.xls")
        sio=StringIO.StringIO()
        ws.save(sio)
        sio.seek(0)
        response=HttpResponse(sio.getvalue(),content_type='application/vnd.ms-excel')
        response['Content-Disposition']='attachment; filename=user.xls'
        response.write(sio.getvalue())
        return response



from user_ex.forms import ChangeNicknameForm,BindEmailForm
from user_ex.models import Profile

def change_nickname(request):
    redirect_to=request.GET.get('from',reverse('home'))
    if request.method =='POST':
        #对表单中数据处理  提交数据的操作
        form=ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new=form.cleaned_data['nickname_new']
            profile,created=Profile.objects.get_or_create(user=request.user)
            profile.nickname=nickname_new
            profile.save()
            return redirect(redirect_to)

    else:
        form=ChangeNicknameForm()
    context={}
    context['page_title']='修改昵称'
    context['form_title']='修改昵称'
    context['submit_text']='修改'
    context['return_back_url']=redirect_to
    context['form']=form
    return render(request,'form.html',context)
#编辑昵称
def edit_nickname(request):
    redirect_to=request.GET.get('from',reverse('home'))
    if request.method=='POST':
        form=ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new=form.cleaned_data['nickname_new']
            profile,created=Profile.objects.get_or_create(user=request.user)
            profile.nickname=nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form=ChangeNicknameForm()
    context={}
    context['page_title']='编辑昵称'
    context['form_title']='编辑昵称'
    context['submit_text']='编辑'
    context['return_back_url']=redirect_to
    context['form']=form
    return render(request,'form.html',context)

#绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        # 对表单中数据处理  提交数据的操作
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email=form.cleaned_data['email']
            request.user.email=email
            request.user.save()
            return redirect(redirect_to)

    else:
        form =BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = redirect_to
    context['form'] = form

    return render(request,'bind_email.html',context)
#发送验证码
import string
import random
from django.core.mail import send_mail
def send_verification_code(request):
    email=request.GET.get('email','')
    data={}
    if email !='':
        #生成验证码
        code=''.join(random.sample(string.ascii_letters + string.digits,4))
        request.session['bind_email_code']=code
        #发送邮件
        send_mail(
            '绑定邮箱',
            '验证码：%s' % code,
            '1963119101@qq.com',
            [email],
            fail_silently=False,
        )
        data['code']=code
        data['status']='Success'
    else:
        data['status']='Error'
    return JsonResponse(data)