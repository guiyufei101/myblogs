"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from blog.views import blog_list
from . import views
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),#首页的路由设置
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('changepassword_action/',views.changepassword_action),

    path('blog/',include('blog.urls')),
    path('comment/',include('comment.urls')),
    path('likes/',include('likes.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('',include('post.urls')),
    path('',include('shop.urls')),

    #path('register/',views.register),
    #path('register_action/',views.register_action),
    path('search_post/',views.search_post),

    path('user_info/',views.user_info,name='user_info'),
    path('export/',views.export),
    path('change_nickname/',views.change_nickname),
    path('edit_nickname/',views.edit_nickname),
    #绑定邮箱
    path('bind_email/',views.bind_email),
    path('bind_email_code/',views.send_verification_code),
    path('user_manage/',views.user_manage,name='user_manage'),
    path('usermanage_action/',views.usermanage_action),
    path('user_info/<int:user_pk>',views.user_info,name='user_info'),
    path('user/<int:user_pk>',views.user_detail,name="user_detail"),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    #path('login_for_medal/',views.login_for_medal,name='login_for_madal'),
]
urlpatterns+=static('/media/',document_root=settings.MEDIA_ROOT)
