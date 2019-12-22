from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import UserInfo
# login,authenticate,logout

# Create your views here.


def login(request):
    if request.method == "POST":
        # 验证数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 有数据
        if all((username,password)):
            user = auth.authenticate(username=username,
                                     password=password)
            # 验证成功
            if user:
                auth.login(request,user)
                return redirect(reverse('blog:category_list',kwargs={'category_id': 1}))


    return render(request, 'user/login.html')


def regist(request):
    if request.method == 'POST':
        # 数据收集
        username = request.get('username')
        password = request.get('username')
        email = request.get('email')
        phone = request.get('phone')
        avatar = request.FILES.get("avatar")
        nickname = request.get('nickname')

        if all((username,password,email,phone)):
            # TODO:单个字段值校验
            # TODO:头像字段需要修改头像文件明 以防止重名覆盖问题

            ret = UserInfo.objects.create_user(username=username,
                                               password=password,
                                               email=email,
                                               phone = phone,
                                               avatar = avatar,
                                               nickname = nickname)

            return redirect(reverse('user:login'))

    return render(request, './user/regist.html')
        # 注册

        # 返回登陆页面





# TODO 重写User表，支持头像上传 邮箱验证

# TODO 权限管理 SSO
