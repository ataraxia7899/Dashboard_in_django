from django.urls import path
from . import views

# app_name을 지정하여 URL 네임스페이스를 설정합니다.
app_name = 'pybo'

urlpatterns = [
    # 예: 대시보드 (http://.../pybo/) -> {% url 'pybo:index' %}
    path('', views.index, name='index'),
    # 예: 게시글 목록 (http://.../pybo/post_list/) -> {% url 'pybo:post_list' %}
    path('post_list/', views.post_list, name='post_list'),

    # 게시글 생성, 수정, 삭제 URL (2단계에서 뷰 함수를 구현할 예정입니다)
    path('post/create/', views.post_create, name='post_create'),
    path('post/update/<int:post_id>/', views.post_update, name='post_update'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
]