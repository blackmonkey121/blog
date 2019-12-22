from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.blog.models import Post


# Create your models here.

# TODO: 重写User表添加更详细的信息 例如头像 位置 偏好等
class UserInfo(AbstractUser):
    """
    用户信息表
    """
    phone = models.CharField(max_length=11, blank=False, unique=True, verbose_name='手机号',db_index=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.jpeg", verbose_name="头像")
    nickname = models.CharField(max_length=64, blank=True, default='匿名用户', verbose_name='昵称')
    email = models.EmailField(blank=False,unique=True,db_index=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = "用户"