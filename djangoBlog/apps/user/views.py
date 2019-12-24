from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from itsdangerous import Serializer, SignatureExpired

from .models import UserInfo
from django.conf import settings
from celery import Celery
from celery_task.tasks import send_register_active_email

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')

# Create your views here.


def login(request):
    if request.method == "POST":
        # 验证数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 有数据
        print(username, password)
        if all((username, password)):
            user = auth.authenticate(username=username,
                                     password=password)
            # 验证成功
            print(user)
            if user:
                auth.login(request, user)
                return redirect(reverse('blog:category_list', kwargs={'category_id': 1}))

    return render(request, 'user/login.html')


def regist(request):
    if request.method == 'POST':
        # 数据收集
        username = request.POST.get('username')
        password = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        avatar = request.FILES.get("avatar")
        nickname = request.POST.get('nickname')

        if all((username, password, email, phone)):
            # TODO:单个字段值校验

            user = UserInfo.objects.create_user(username=username,
                                         password=password,
                                         email=email,
                                         phone=phone,
                                         avatar=avatar,
                                         nickname=nickname)

            # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
            # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

            # 加密用户的身份信息，生成激活token
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.id}
            token = serializer.dumps(info)  # bytes
            token = token.decode()

            # 发邮件
            send_register_active_email.delay(email, username, token)


            return redirect(reverse('user:login'))

    print("regist.html")
    return render(request, './user/regist.html')
    # 注册

    # 返回登陆页面


def active(request, token):

    '''进行用户激活'''
    # 进行解密，获取要激活的用户信息
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        # 获取待激活用户的id
        user_id = info['confirm']

        # 根据id获取用户信息
        user = UserInfo.objects.get(id=user_id)
        user.is_active = 1
        user.save()

        # 跳转到登录页面
        return redirect(reverse('user:login'))
    except SignatureExpired as e:
        # 激活链接已过期
        return HttpResponse('激活链接已过期')


# TODO 重写User表，支持头像上传 邮箱验证

# TODO 权限管理 SSO
