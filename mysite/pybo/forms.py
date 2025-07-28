from django import forms
from django.contrib.auth.models import User as AuthUser
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': '제목',
            'content': '내용',
        }

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = AuthUser # Django의 기본 User 모델 사용
        fields = ['username']
        labels = {
            'username': '사용자 ID',
        }

    def clean_password2(self):
        # 비밀번호 2개가 일치하는지 확인
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return cd.get('password2')