from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookmark, Post, User, PostLike, Comment
from django.utils import timezone
from datetime import timedelta
import json, collections
from django.db.models import Count
from django.db.models.functions import TruncDay

# Create your views here.
def index(request):
    # --- 1. Status Card 데이터 계산 ---
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_likes = PostLike.objects.count()
    total_comments = Comment.objects.count()
    total_bookmarks = Bookmark.objects.count()

    # 30일 내 활동한 사용자 (MAU)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_user_ids = set()
    active_user_ids.update(Post.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True))
    active_user_ids.update(Comment.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True))
    active_user_ids.update(PostLike.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True))
    monthly_active_users = len(active_user_ids)

    # --- 2. Chart 데이터 준비 (JSON으로 변환) ---
    # Pie Chart
    pie_chart_data = {
        'labels': ['게시글', '좋아요', '댓글', '북마크'],
        'data': [total_posts, total_likes, total_comments, total_bookmarks]
    }

    # DAU Chart (지난 30일간 실제 활동 사용자 기준)
    # 1. 모든 활동을 수집합니다.
    post_activities = Post.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at')
    comment_activities = Comment.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at')
    like_activities = PostLike.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at')
    bookmark_activities = Bookmark.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at')
    all_activities = list(post_activities) + list(comment_activities) + list(like_activities) + list(bookmark_activities)

    # 2. 날짜별로 고유한 사용자 ID를 집계합니다.
    daily_active_users = collections.defaultdict(set)
    for activity in all_activities:
        if activity['user_id']:
            activity_date = activity['created_at'].date()
            daily_active_users[activity_date].add(activity['user_id'])

    # 3. 차트 라벨과 데이터를 생성합니다 (활동이 없는 날은 0으로 채움).
    dau_labels = []
    dau_values = []
    today = timezone.now().date()
    for i in range(30):
        current_date = today - timedelta(days=29 - i)
        dau_labels.append(current_date.strftime('%m/%d'))
        dau_values.append(len(daily_active_users.get(current_date, set())))

    # --- 3. List 데이터 준비 ---
    recent_users = User.objects.order_by('-join_date')[:5]
    # select_related('user')는 Post와 연결된 User 정보를 미리 가져와 DB 조회를 최적화합니다.
    recent_posts = Post.objects.select_related('user').order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'monthly_active_users': monthly_active_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_bookmarks': total_bookmarks,
        'pie_chart_data_json': json.dumps(pie_chart_data),
        'dau_labels_json': json.dumps(dau_labels),
        'dau_values_json': json.dumps(dau_values),
        'recent_users': recent_users,
        'recent_posts': recent_posts,
    }
    return render(request, 'dashboard.html', context)

def post_list(request):
  # post_list 뷰도 실제 데이터를 조회하도록 개선합니다.
  posts = Post.objects.select_related('user').order_by('-created_at')
  return render(request, 'post_list.html', {'posts': posts})