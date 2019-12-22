from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import UserInfo


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
            # TODO:头像字段需要修改头像文件明 以防止重名覆盖问题

            UserInfo.objects.create_user(username=username,
                                         password=password,
                                         email=email,
                                         phone=phone,
                                         avatar=avatar,
                                         nickname=nickname)


            return redirect(reverse('user:login'))

    print("regist.html")
    return render(request, './user/regist.html')
    # 注册

    # 返回登陆页面

# TODO 重写User表，支持头像上传 邮箱验证

# TODO 权限管理 SSO
