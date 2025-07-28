from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name을 지정하여 URL 네임스페이스를 설정합니다.
app_name = 'pybo'

urlpatterns = [
    # 예: 대시보드 (http://.../pybo/) -> {% url 'pybo:index' %}
    path('dashboard/', views.index, name='index'),
    # 예: 게시글 목록 (http://.../pybo/post_list/) -> {% url 'pybo:post_list' %}
    path('post_list/', views.post_list, name='post_list'),
    
    # 게시글 상세, 생성, 수정, 삭제 URL
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/update/<int:post_id>/', views.post_update, name='post_update'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),

    # 로그인/로그아웃 URL 추가
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]