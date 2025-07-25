from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Bookmark, Post, User, PostLike, Comment
from .forms import PostForm
from django.utils import timezone
from datetime import timedelta
import json, collections
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # --- 1. Status Card 데이터 계산 ---
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_likes = PostLike.objects.count()
    total_comments = Comment.objects.count()
    total_bookmarks = Bookmark.objects.count()

    # [개선] 30일 내 활동한 사용자 (MAU) 계산 최적화
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # 각 활동에서 사용자 ID를 가져오는 쿼리셋을 정의합니다.
    post_users = Post.objects.filter(created_at__gte=thirty_days_ago, user__isnull=False).values_list('user_id', flat=True)
    comment_users = Comment.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True)
    like_users = PostLike.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True)
    bookmark_users = Bookmark.objects.filter(created_at__gte=thirty_days_ago).values_list('user_id', flat=True)
    # union으로 쿼리셋을 합치고, 고유한 사용자의 수를 DB에서 직접 계산합니다.
    # [수정] union()은 기본적으로 중복을 제거하므로 .distinct()는 필요 없으며, 함께 사용 시 에러가 발생합니다.
    monthly_active_users = post_users.union(comment_users, like_users, bookmark_users).count()

    # --- 2. Chart 데이터 준비 (JSON으로 변환) ---
    # Pie Chart
    pie_chart_data = {
        'labels': ['게시글', '좋아요', '댓글', '북마크'],
        'data': [total_posts, total_likes, total_comments, total_bookmarks]
    }

    # [수정] DAU Chart 계산 로직 변경
    # union() 이후에는 annotate() 등 추가적인 DB 연산이 불가능하므로, Python에서 데이터를 집계합니다.
    # 1. 모든 활동 기록을 하나의 쿼리셋으로 가져옵니다.
    all_activities_query = Post.objects.filter(created_at__gte=thirty_days_ago, user__isnull=False).values('user_id', 'created_at') \
        .union(
            Comment.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at'),
            PostLike.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at'),
            Bookmark.objects.filter(created_at__gte=thirty_days_ago).values('user_id', 'created_at')
        )

    # 2. Python에서 날짜별로 고유한 사용자 ID를 집계합니다.
    daily_active_users = collections.defaultdict(set)
    for activity in all_activities_query:
        if activity['user_id']:
            # Django의 timezone-aware datetime 객체에서 date()를 추출합니다.
            activity_date = activity['created_at'].date()
            daily_active_users[activity_date].add(activity['user_id'])

    # 3. 차트 라벨과 데이터를 생성합니다 (활동이 없는 날은 0으로 채웁니다).
    dau_labels = []
    dau_values = []
    today = timezone.now().date()
    for i in range(30):
        current_date = today - timedelta(days=29 - i)
        dau_labels.append(current_date.strftime('%m/%d'))
        # daily_active_users 딕셔너리에서 해당 날짜의 set을 가져오고, 그 길이를 구합니다.
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
  # 페이지네이션 추가
  page = request.GET.get('page', '1') # 페이지
  post_list = Post.objects.select_related('user').order_by('-created_at')
  paginator = Paginator(post_list, 10) # 페이지당 10개씩 보여주기
  page_obj = paginator.get_page(page)
  return render(request, 'post_list.html', {'posts': page_obj})

def post_detail(request, post_id):
    """
    post_id에 해당하는 게시글의 상세 정보를 보여주는 뷰
    """
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'post_detail.html', context)


def post_create(request):
    # [개선] get_or_create를 사용하여 사용자가 없으면 생성하고, 있으면 가져옵니다.
    # 이렇게 하면 코드가 더 안정적이고 간결해집니다.
    # 실제 서비스에서는 request.user를 사용해야 합니다.
    default_user, created = User.objects.get_or_create(username='admin_user')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = default_user
            post.save()
            return redirect('pybo:post_list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'post_form.html', context)

def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('pybo:post_list')
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'post_form.html', context)

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST': # POST 요청일 때만 삭제
        post.delete()
    return redirect('pybo:post_list')