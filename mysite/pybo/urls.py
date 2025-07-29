from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name을 지정하여 URL 네임스페이스를 설정합니다.
app_name = 'pybo'

urlpatterns = [
    # 예: 대시보드 (http://.../pybo/) -> {% url 'pybo:index' %}
    path('dashboard/', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
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

	# 좋아요, 북마크 기능 URL
	path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
	path('post/<int:post_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    # 댓글 기능 URL
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]