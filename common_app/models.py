from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# 유저 권한
USER_GRADE = [
    (0, '관리자'),
    (1, '일반 사용자'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom 헬퍼 클래스를 사용하도록 설정
    objects = UserManager()

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'  # Username을 email로 명시

    # 이름 - ID 역할
    name = models.CharField(
        verbose_name='name',
        max_length=20,
        null=False
    )

    user_grade = models.IntegerField(
        choices=USER_GRADE,
        default=1,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # REQUIRED_FIELDS 안 쓰면 createsuperuser 할 때 안 나타남
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    # 커스텀 유저 모델을 기본 유저 모델로 사용하기 위해 구현한 부분
    #   True를 반환하여 권한이 있음을 알림
    def has_perm(self, perm, obj=None):
        return True
    #   True를 반환하여 주어진 App의 모델에 접근 가능하도록 함
    def has_module_perms(self, app_label):
        return True
    #   True 가 반환되면 관리자 화면에 로그인 가능
    @property
    def is_staff(self):
        return self.is_admin
