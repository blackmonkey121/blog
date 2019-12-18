from django.shortcuts import render, HttpResponse


# Create your views here.


def index(request):
    return HttpResponse("Anything is OK!")

# TODO 重写User表，支持头像上传 邮箱验证
