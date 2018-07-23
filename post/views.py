from django.shortcuts import render,render_to_response,get_object_or_404
from .models import Post,Comment
from .forms import EmailPostForm,CommentForm
# Create your views here.

def post_list(request):
    posts=Post.objects.all()
    context={}
    context['posts']=posts
    return render(request,'post_list.html',context)

def post_detail(request,post_pk):
    context = {}
    post = get_object_or_404(Post, pk=post_pk)
    comments=Comment.objects.filter(active=True,post=post)
    context['post']=post
    context['comments']=comments
    if request.method == 'POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
        else:
            comment_form=CommentForm()
        context['new_comment']=new_comment
        context['comment_form']=comment_form
    return render(request,'post_detail.html',context)

def post_share(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)
    context={}
    '''if request.method == 'POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
        else:
            form=EmailPostForm()
        context['form']=form
        context['post']=post'''
    context['post']=post
    return render(request,'post_share.html',context)
