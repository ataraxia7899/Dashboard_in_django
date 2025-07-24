# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Bookmark(models.Model):
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bookmark'


class Comment(models.Model):
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment'


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post'


class PostLike(models.Model):
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post_like'


class User(models.Model):
    username = models.CharField(unique=True, max_length=50)
    join_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'