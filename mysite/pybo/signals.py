from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser
from django.urls import reverse
from .models import Post, Comment, PostLike, ActivityLog, User as PyboUser

@receiver(post_save, sender=AuthUser)
def create_signup_log(sender, instance, created, **kwargs):
    """사용자가 가입했을 때 활동 로그를 생성합니다."""
    if created:
        pybo_user, _ = PyboUser.objects.get_or_create(username=instance.username)
        ActivityLog.objects.create(
            user=pybo_user,
            activity_type='signup',
            message=f"<strong>{instance.username}</strong>님이 새로 가입했습니다."
        )

@receiver(post_save, sender=Post)
def create_post_log(sender, instance, created, **kwargs):
    """게시글이 작성되었을 때 활동 로그를 생성합니다."""
    post_url = reverse('pybo:post_detail', args=[instance.id])
    if created:
        ActivityLog.objects.create(
            user=instance.user,
            activity_type='post',
            message=f"<strong>{instance.user.username}</strong>님이 새 게시글 <a href='{post_url}'>'{instance.title}'</a>을(를) 작성했습니다."
        )
    else:
        # 게시글 수정 시 로그
        ActivityLog.objects.create(
            user=instance.user,
            activity_type='post',
            message=f"<strong>{instance.user.username}</strong>님이 게시글 <a href='{post_url}'>'{instance.title}'</a>을(를) 수정했습니다."
        )

@receiver(post_save, sender=Comment)
def create_comment_log(sender, instance, created, **kwargs):
    """댓글이 작성되었을 때 활동 로그를 생성합니다."""
    if created:
        post_author_username = instance.post.user.username if instance.post.user else "(알 수 없음)"
        message = f"<strong>{instance.user.username}</strong>님이 <strong>{post_author_username}</strong>님의 게시글에 댓글을 남겼습니다."
        ActivityLog.objects.create(
            user=instance.user,
            activity_type='comment',
            message=message
        )

@receiver(post_save, sender=PostLike)
def create_like_log(sender, instance, created, **kwargs):
    """좋아요를 눌렀을 때 활동 로그를 생성합니다."""
    if created:
        post_author_username = instance.post.user.username if instance.post.user else "(알 수 없음)"
        message = f"<strong>{instance.user.username}</strong>님이 <strong>{post_author_username}</strong>님의 게시글을 좋아합니다."
        ActivityLog.objects.create(
            user=instance.user,
            activity_type='like',
            message=message
        )

@receiver(post_delete, sender=Post)
def delete_post_log(sender, instance, **kwargs):
    """게시글이 삭제되었을 때 활동 로그를 생성합니다."""
    ActivityLog.objects.create(
        user=instance.user,
        activity_type='post',
        message=f"<strong>{instance.user.username}</strong>님이 게시글 '{instance.title}'을(를) 삭제했습니다."
    )

@receiver(post_delete, sender=PostLike)
def delete_like_log(sender, instance, **kwargs):
    """좋아요가 취소(삭제)되었을 때 활동 로그를 생성합니다."""
    post_author_username = instance.post.user.username if instance.post.user else "(알 수 없음)"
    message = f"<strong>{instance.user.username}</strong>님이 <strong>{post_author_username}</strong>님의 게시글에 대한 좋아요를 취소했습니다."
    ActivityLog.objects.create(
        user=instance.user,
        activity_type='like',
        message=message
    )