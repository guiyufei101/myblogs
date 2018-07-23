from django.urls import path
from . import views

urlpatterns=[
    path('product_list',views.product_list,name='product_list'),
    path('product/<int:product_pk>', views.product_detail, name="product_detail"),
]