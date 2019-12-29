from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


# TODO: 重写User表添加更详细的信息 例如头像 位置 偏好等
class UserInfo(AbstractUser):
    """
    用户信息表
    """
    phone = models.CharField(max_length=11, blank=True, unique=True, verbose_name='手机号',db_index=True,default=00000000000)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.jpeg", verbose_name="头像")
    nickname = models.CharField(max_length=64, blank=True, default='匿名用户', verbose_name='昵称')
    email = models.EmailField(blank=False,unique=True,db_index=True)
    is_check = models.BooleanField(blank=False, default=False, verbose_name="email是否验证")
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = "用户"