from django.db import models

from common_app.models import User
from z_diary_proj import settings


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
    )

    description = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    # 사용자
    user_id = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        db_column='user_id',  # account 실제 DB 스키마의 컬럼 이름
    )

    # 카테고리
    category_id = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.CASCADE,
        db_column='category_id',
    )

    date = models.DateField(null=False)
    amount = models.IntegerField(null=False)
    description = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', ]
