from django.shortcuts import render, HttpResponse


# Create your views here.


def index(request):
    return render(request, 'blog/article.html')

# TODO 重写User表，支持头像上传 邮箱验证

# TODO 权限管理 SSO
