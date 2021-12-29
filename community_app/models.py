from django.db import models

from z_diary_proj import settings


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
    )

    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    category_id = models.ForeignKey(
        Category,
        related_name='post_category',
        on_delete=models.SET_NULL,
        db_column='category_id',
        null=True,
    )

    title = models.CharField(max_length=20)
    content = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post,
        related_name='post_comment',
        on_delete=models.CASCADE,
        db_column='post_id'
    )

    comment = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)