from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class User(AbstractUser):
    # TODO: 加入头像、默认头像
    nickname = models.CharField('昵称', max_length=20, blank=True,)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    link = models.CharField('个人网址', max_length=30, blank=True, default=None, null=True)
    email = models.EmailField('电子邮箱', unique=True,
                              error_messages={'unique': "电子邮箱已存在", },)

    # 绑定第三方账号

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
