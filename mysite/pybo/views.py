from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Bookmark, Post, User, PostLike, Comment, DailyVisitor, ActivityLog
from .forms import PostForm, SignUpForm, CommentForm
from django.utils import timezone
from datetime import timedelta
import json, collections
from django.db.models import Count
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import views as auth_views, login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import TruncDate
from django.db import transaction
from django.core.paginator import Paginator

@login_required(login_url='pybo:login')
@user_passes_test(lambda u: u.is_superuser, login_url='pybo:post_list')
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

    # 오늘의 방문자 수 (DailyVisitor 모델에서 가져오기)
    today = timezone.now().date()
    today_visitors_record = DailyVisitor.objects.filter(date=today).first()
    today_visitors = today_visitors_record.count if today_visitors_record else 0

    # --- 3. List 데이터 준비 ---
    recent_users = User.objects.order_by('-join_date')[:5]
    # select_related('user')는 Post와 연결된 User 정보를 미리 가져와 DB 조회를 최적화합니다.
    recent_posts = Post.objects.select_related('user').order_by('-created_at')[:5]
    recent_activities = ActivityLog.objects.select_related('user').order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'monthly_active_users': monthly_active_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_bookmarks': total_bookmarks,
        'today_visitors': today_visitors,
        'pie_chart_data_json': json.dumps(pie_chart_data),
        'dau_labels_json': json.dumps(dau_labels),
        'dau_values_json': json.dumps(dau_values),
        'recent_users': recent_users,
        'recent_posts': recent_posts,
        'recent_activities': recent_activities,
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
    post = get_object_or_404(Post.objects.select_related('user'), pk=post_id)
    
    # 댓글 목록과 댓글 폼
    comments = post.comments.select_related('user').order_by('created_at')
    comment_form = CommentForm()

    # 좋아요, 북마크 상태 확인 (로그인한 경우에만)
    is_liked = False
    is_bookmarked = False
    if request.user.is_authenticated:
        # [FIX] 두 종류의 User 모델 혼용으로 인한 ORM 오류를 피하기 위해 직접 모델을 쿼리합니다.
        # post.likes.filter() 대신 PostLike.objects.filter()를 사용합니다.
        # [FIX 2] user 객체 대신 user.id를 사용하여 타입 에러를 회피합니다.
        is_liked = PostLike.objects.filter(post=post, user_id=request.user.id).exists()
        is_bookmarked = Bookmark.objects.filter(post=post, user_id=request.user.id).exists()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'post_detail.html', context)


@login_required(login_url='pybo:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Django의 로그인 유저(request.user)와 pybo의 User 모델을 연결합니다.
            pybo_user, created = User.objects.get_or_create(username=request.user.username)
            post = form.save(commit=False)
            post.user = pybo_user
            post.save()
            return redirect('pybo:post_list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'post_form.html', context)

@login_required(login_url='pybo:login')
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # 작성자 본인 또는 관리자가 아니면 권한 없음 처리
    if request.user.username != post.user.username and not request.user.is_superuser:
        messages.error(request, '이 게시글을 수정할 권한이 없습니다.')
        return redirect('pybo:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # 수정 후 목록 대신 상세 페이지로 이동하여 사용자 경험 개선
            return redirect('pybo:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'post_form.html', context)

@login_required(login_url='pybo:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # 작성자 본인 또는 관리자가 아니면 권한 없음 처리
    if request.user.username != post.user.username and not request.user.is_superuser:
        messages.error(request, '이 게시글을 삭제할 권한이 없습니다.')
        return redirect('pybo:post_detail', post_id=post.id)

    if request.method == 'POST': # POST 요청일 때만 삭제
        post.delete()
        messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
    return redirect('pybo:post_list')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # transaction.atomic을 사용하여 두 생성 작업을 하나의 트랜잭션으로 묶습니다.
            # 이렇게 하면 둘 중 하나라도 실패할 경우 모든 변경사항이 롤백됩니다.
            with transaction.atomic():
                # 1. Django의 인증용 User 생성
                auth_user = form.save(commit=False)
                auth_user.set_password(form.cleaned_data['password'])
                auth_user.save()

                # 2. 우리 앱의 User 모델과 연결하여 생성
                # get_or_create를 사용하여 혹시라도 pybo_user가 이미 존재하는 경우
                # 오류 대신 기존 객체를 가져오도록 하여 안정성을 높입니다.
                User.objects.get_or_create(username=auth_user.username)

                # 3. 회원가입 후 자동 로그인 및 리디렉션
                auth_login(request, auth_user)
                return redirect('pybo:post_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='pybo:login')
@user_passes_test(lambda u: u.is_superuser, login_url='pybo:post_list')
def user_list(request):
    """관리자만 접근 가능한 사용자 목록 페이지"""
    if not request.user.is_superuser:
        return HttpResponseForbidden('관리자만 접근할 수 있는 페이지입니다.')

    # Django의 기본 User 모델을 사용하여 모든 사용자를 가져옵니다.
    all_users = AuthUser.objects.all().order_by('-date_joined')

    context = {
        'users': all_users,
    }
    return render(request, 'user_list.html', context)

class CustomLoginView(auth_views.LoginView):
    """로그인 성공 후 사용자의 is_superuser 값에 따라 리디렉션 경로를 다르게 처리합니다."""
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return reverse_lazy('pybo:index')  # 관리자는 대시보드로
            else:
                return reverse_lazy('pybo:post_list') # 일반 사용자는 글 목록으로
        
        # 인증되지 않은 경우 (이론적으로는 도달하지 않음)
        return reverse_lazy('pybo:login')

@login_required(login_url='pybo:login')
@user_passes_test(lambda u: u.is_superuser, login_url='pybo:post_list')
def user_delete(request, user_id):
    """관리자만 사용자를 삭제할 수 있는 기능. auth_user와 pybo_user 모두 삭제합니다."""
    # POST 요청일 때만 삭제를 처리합니다.
    if request.method == 'POST':
        # 삭제할 Django 인증 사용자 객체를 가져옵니다.
        user_to_delete = get_object_or_404(AuthUser, pk=user_id)
        
        # 현재 로그인한 관리자가 자기 자신을 삭제하려는 경우를 방지합니다.
        if request.user.id == user_to_delete.id:
            messages.error(request, '자기 자신은 삭제할 수 없습니다.')
        else:
            # 두 테이블의 삭제 작업을 하나의 트랜잭션으로 묶어 데이터 일관성을 보장합니다.
            try:
                with transaction.atomic():
                    username = user_to_delete.username
                    
                    # 1. pybo 앱의 User 모델에서 해당 사용자 삭제
                    #    - filter().delete()는 대상이 없어도 오류를 발생시키지 않아 안전합니다.
                    User.objects.filter(username=username).delete()
                    
                    # 2. Django의 인증 User 모델에서 사용자 삭제
                    #    - 이 작업이 실행되면 관련 Post, Comment 등도 on_delete 정책에 따라 처리됩니다.
                    user_to_delete.delete()
                    
                    messages.success(request, f'사용자 "{username}" 님을 성공적으로 삭제했습니다.')
            except Exception as e:
                # 트랜잭션 중 오류 발생 시 사용자에게 알립니다.
                messages.error(request, f'사용자 삭제 중 오류가 발생했습니다: {e}')
            
    # 처리 후에는 항상 사용자 목록 페이지로 리디렉션합니다.
    return redirect('pybo:user_list')

@login_required(login_url='pybo:login')
def toggle_bookmark(request, post_id):
    """AJAX 요청을 받아 게시글의 북마크 상태를 토글합니다."""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        pybo_user, _ = User.objects.get_or_create(username=request.user.username)

        bookmark, created = Bookmark.objects.get_or_create(
            post=post,
            user=pybo_user
        )

        if not created:
            # 북마크가 이미 존재하면 삭제합니다.
            bookmark.delete()
            is_bookmarked = False
        else:
            # 새로 생성되었으면 상태를 True로 설정합니다.
            is_bookmarked = True
        
        # JSON 응답으로 현재 북마크 상태와 총 북마크 수를 반환합니다.
        return JsonResponse({'is_bookmarked': is_bookmarked, 'bookmark_count': post.bookmarks.count()})
    
    # POST 요청이 아니면 상세 페이지로 리디렉션합니다.
    return redirect('pybo:post_detail', post_id=post_id)

@login_required(login_url='pybo:login')
def toggle_like(request, post_id):
    """AJAX 요청을 받아 게시글의 좋아요 상태를 토글합니다."""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        pybo_user, _ = User.objects.get_or_create(username=request.user.username)

        like, created = PostLike.objects.get_or_create(
            post=post,
            user=pybo_user
        )

        if not created:
            # 이미 좋아요를 눌렀으면 취소합니다.
            like.delete()
            is_liked = False
        else:
            # 새로 생성되었으면 상태를 True로 설정합니다.
            is_liked = True
        
        # JSON 응답으로 현재 좋아요 상태와 총 좋아요 수를 반환합니다.
        return JsonResponse({'is_liked': is_liked, 'like_count': post.likes.count()})
    
    # POST 요청이 아니면 상세 페이지로 리디렉션합니다.
    return redirect('pybo:post_detail', post_id=post_id)

@login_required(login_url='pybo:login')
def add_comment(request, post_id):
    """댓글을 추가합니다."""
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            # [FIX] request.user (AuthUser)를 pybo.models.User로 변환합니다.
            pybo_user, _ = User.objects.get_or_create(username=request.user.username)
            comment.user = pybo_user

            comment.save()
            messages.success(request, '댓글이 성공적으로 등록되었습니다.')
        else:
            # 폼이 유효하지 않을 경우, 오류 메시지를 표시합니다.
            messages.error(request, '댓글 내용에 오류가 있습니다. 다시 시도해주세요.')
    # 처리 후에는 항상 게시글 상세 페이지로 리디렉션합니다.
    return redirect('pybo:post_detail', post_id=post.id)

@login_required(login_url='pybo:login')
def comment_update(request, comment_id):
    """댓글을 수정합니다."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.username != comment.user.username:
        messages.error(request, '댓글을 수정할 권한이 없습니다.')
        return redirect('pybo:post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('pybo:post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comment_form.html', {'form': form, 'comment': comment})

@login_required(login_url='pybo:login')
def delete_comment(request, comment_id):
    """댓글을 삭제합니다."""
    comment = get_object_or_404(Comment, pk=comment_id)
    # [FIX] 다른 User 모델 간의 비교 오류를 수정하고, 사용자 이름으로 권한을 확인합니다.
    if request.user.username != comment.user.username and not request.user.is_superuser:
        messages.error(request, '댓글을 삭제할 권한이 없습니다.')
        return redirect('pybo:post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        messages.success(request, '댓글이 성공적으로 삭제되었습니다.')
        return redirect('pybo:post_detail', post_id=post_id)
    
    # POST 요청이 아니면 해당 댓글이 있는 상세 페이지로 리디렉션합니다.
    return redirect('pybo:post_detail', post_id=comment.post.id)