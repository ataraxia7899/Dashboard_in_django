from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post

# Create your views here.
def index(request):
  # 대시보드에 필요한 데이터 조회
  total_users = User.objects.count()
  total_posts = Post.objects.count()
  recent_posts = Post.objects.order_by('-created_at')[:5] # 최근 5개 게시글

  context = {
      'total_users': total_users,
      'total_posts': total_posts,
      'recent_posts': recent_posts,
      # 좋아요, 댓글 등 다른 통계는 관련 모델 추가 후 구현 가능
  }
  return render(request, 'dashboard.html', context)

def post_list(request):
  # 모든 게시글을 최신순으로 조회
  posts = Post.objects.order_by('-created_at').all()
  context = {
      'posts': posts,
  }
  return render(request, 'post_list.html', context)