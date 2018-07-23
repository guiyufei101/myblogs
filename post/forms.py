from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name=forms.CharField(label='用户名',min_length=2,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailField())
    to=forms.EmailField(label='接收邮箱',widget=forms.EmailField())
    comments=forms.CharField(required=False,widget=forms.Textarea)
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')