from django.urls import path
from . import views
urlpatterns=[
    path('post_list',views.post_list),
    path('<int:post_pk>',views.post_detail,name="post_detail"),
    path('post/<int:post_pk>',views.post_share,name='post_share'),
]