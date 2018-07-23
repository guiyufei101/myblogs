from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.utils import timezone
from django.db.models import Sum
import datetime
def read_statistics_once_read(request,obj):#对应博客的阅读计数
    ct=ContentType.objects.get_for_model(obj)
    key="%s_%s_read" % (ct.model,obj.pk)
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
            readnum=ReadNum.objects.get(content_type=ct,object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()
        else:
            readnum=ReadNum(content_type=ct,object_id=obj.pk)
            readnum.read_num = 1
            readnum.save()
        # 每天的计数
        date = timezone.now().date()#打开博客的时刻记录下来
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
            readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)#取记录并且能够取到记录
            readDetail.read_num += 1
            readDetail.save()
        else:#不存在记录也就是说没有阅读过的
            readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)#创建对象并且赋值阅读数为1
            readDetail.read_num = 1
            readDetail.save()
    return key
def get_seven_days_read_data(content_type):
    # 七天计数
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))#分组统计
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details=ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')#排序倒序
    return read_details
def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date()-datetime.timedelta(days=1)#昨天
    read_details=ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')#排序倒序
    return read_details
#一周的点击数据
def get_seventdays_hot_data(content_type):
    today = timezone.now().date()
    date=today-datetime.timedelta(days=7)
    read_details=ReadDetail.objects.filter(content_type=content_type,date__lt=today,date__gt=date)\
        .values('content_type','object_id')\
        .annotate(read_num_sum=Sum('read_num'))\
        .order_by('-read_num_sum')#排序倒序  用天数小于今天且大于7天前来表示一周的数量
    return read_details[:7]#返回前7个