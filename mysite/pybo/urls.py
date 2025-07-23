from django.urls import path
from . import views

# app_name을 지정하여 URL 네임스페이스를 설정합니다.
app_name = 'pybo'

urlpatterns = [
    # 예: 대시보드 (http://.../pybo/) -> {% url 'pybo:index' %}
    path('', views.index, name='index'),
    # 예: 게시글 목록 (http://.../pybo/post_list/) -> {% url 'pybo:post_list' %}
    path('post_list/', views.post_list, name='post_list'),
]