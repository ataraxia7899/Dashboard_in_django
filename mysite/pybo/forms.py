from django import forms
from django.contrib.auth.models import User as AuthUser
from .models import Post, Comment, Bookmark, PostLike

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'attachment']
        labels = {
            'title': '제목',
            'content': '내용',
            'attachment': '첨부파일',
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
    
class CommentForm(forms.ModelForm):
    """댓글 작성을 위한 폼"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-input', # 기존 스타일과 통일
                    'rows': 3,
                    'placeholder': '댓글을 남겨주세요'
                }
            ),
        }
        labels = { 'content': '' } # <label> 태그를 표시하지 않음