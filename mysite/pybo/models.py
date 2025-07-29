# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class User(models.Model):
    username = models.CharField(unique=True, max_length=50)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/', blank=True, null=True, verbose_name='첨부파일')

    def __str__(self):
        return self.title

    @property
    def is_image(self):
        """첨부파일이 이미지 형식인지 확인하는 속성"""
        if self.attachment:
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            return any(self.attachment.name.lower().endswith(ext) for ext in image_extensions)
        return False

    class Meta:
        db_table = 'post'


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmark'
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'

    class Meta:
        db_table = 'comment'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_like'
        unique_together = ('user', 'post')


class DailyVisitor(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'daily_visitor'