from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label ='新的昵称',
        max_length=20,
        widget =forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'请输入新的昵称'
            }
        )
    )
    def __init__(self,*args,**kwargs):#两个任意类型的参数
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(ChangeNicknameForm,self).__init__(*args,**kwargs)

    def clean(self):
        #判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data
    def clean_nickname_new(self):
        nickname_new=self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise  forms.ValidationError("新的昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email=forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入正确的邮箱'
            }
        )
    )
    #验证码
    verification_code=forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self,*args,**kwargs):#两个任意类型的参数
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm,self).__init__(*args,**kwargs)

    def clean(self):
        #判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user']=self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        #判断用户是否绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')
        #判断验证码
        code= self.request.session.get('bind_email_code','')
        verification_code=self.cleaned_data.get('verification_code','')
        if  not (code !='' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data


    def clean_email(self):
        #获取email
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email
    def  clean_verification_code(self):
        verification_code=self.cleaned_data.get('verification_code','').strip()
        if verification_code=='':
            raise forms.ValidationError('验证吗不能为空')
        return verification_code
