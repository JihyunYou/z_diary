from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from common_app.models import User
from z_diary_proj import settings


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
    )

    description = models.TextField()

    order = models.IntegerField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', ]


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
        on_delete=models.SET_NULL,
        db_column='category_id',
        null=True
    )

    date = models.DateField(null=False)
    amount = models.IntegerField(null=False)
    description = models.TextField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', ]

    def get_sum_by_category(self, user_id, year, month):
        result = Account.objects.filter(
            user_id=user_id,
            date__year=year,
            date__month=month,
        ).values('category_id').order_by('category_id').annotate(
            sum_amount=Coalesce(Sum('amount'), Value(0))
        )

        return result