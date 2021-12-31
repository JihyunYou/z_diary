from django.db import models

from z_diary_proj import settings


class Subject(models.Model):
    name = models.CharField(
        max_length=10,
        null=False,
    )

    description = models.TextField()

    is_admin = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        db_column='category_id',
        null=True,
    )

    title = models.CharField(max_length=30)
    content = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        db_column='post_id'
    )

    comment = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)