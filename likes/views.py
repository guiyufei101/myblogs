from django.shortcuts import render
from .models import LikeRecord,LikeCount
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
# Create your views here.
def ErrorResponse(code,message):
    data={}
    data['status']='ERROR'
    data['code']=code
    data['message']=message
    return  JsonResponse(data)
def SuccessResponse(liked_num):
    data={}
    data['status']='SUCCESS'
    data['liked_num']=liked_num
    return JsonResponse(data)

def like_change(request):
    #获取数据
    user=request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'你没有登录')

    content_type=request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'对象不存在')

    is_like=request.GET.get('is_like')
    #处理数据
    if is_like =='true':
        #要点赞的
        like_record,created=LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created:
            #未点赞过进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return  SuccessResponse(like_count.liked_num)
        else:
            #已经点过赞的，不能重复点赞
            return  ErrorResponse(402,'你已经点赞过')

    else:
        #取消点赞的
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            like_record=LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            #d点赞数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                #点过赞的
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404,'你没有点过赞')
        else:
            #没有点赞过，不能取消
            return ErrorResponse(403,'你没有点赞过')
