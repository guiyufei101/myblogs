from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.

def product_list(request,category_slug=None):
    context={}
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    context['category']=category
    context['products']=products
    context['categories']=categories

    page_num = request.GET.get('page', 1)  # 获取url页面参数get请求
    paginator = Paginator(products, 9)  # 每9篇进行分页
    page_of_products = paginator.get_page(page_num)  # 得到页码所对应的页面
    context['page_of_products'] = page_of_products
    # 获取当前页
    current_page_num = page_of_products .number
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
    context['current_page'] = current_page_num
    return render(request,'product_list.html',context)

def product_detail(request,product_pk):
    product=get_object_or_404(Product,pk=product_pk)
    now=datetime.now()
    context={}
    context['product']=product
    context['time']=now
    # 获取上一条博客
    context['previous_product'] = Product.objects.filter(created__gt=product.created).last()
    # 获取下一条博客
    context['next_product']=Product.objects.filter(created__lt=product.created).first()
    return  render(request,'product_detail.html',context)
