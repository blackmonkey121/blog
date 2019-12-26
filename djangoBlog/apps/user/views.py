from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired

from .models import UserInfo
from django.conf import settings
from celery import Celery
from celery_task.tasks import send_register_active_email
from re import match
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')

# Create your views here.
class CheckData(object):
    def __init__(self,args_list, **kwargs):

        self.key_list = args_list  # 确保前端提交的数据完整
        self.data = kwargs
        self.data.pop('csrfmiddlewaretoken')
        self.error_dict = {}    # 错误信息字典

        if set(self.key_list).issubset(set(self.data.keys())):
            self.__merge_password()
        else:
            self.error_dict["info"] = "必填信息不完整"

    def __merge_password(self):
        """
        合并password  和 repassword
        self.data -> "password":[password, repassword]
        :return:
        """
        if "repassword" in self.data.keys():
            self.data['password'] = [self.data.get('password')[0], self.data.get('repassword')[0]]
            self.data.pop('repassword')

    def check_username(self, username):
        if not 17 > len(username) > 1:
            self.error_dict['username'] = "必填项：2~16个字符"
        # TODO: 敏感词检测

    def check_nickname(self, nickname):
        # TODO: 调用接口进行敏感词检测
        pass

    def check_password(self, pwd, repwd=None):
        """
        检测密码和重复密码是否一致
        :param pwd: 密码
        :param repwd: 重复密码
        """
        if not 21 > len(pwd) > 5:
            self.error_dict['password'] = "必填项：5～20个字符"

        elif pwd != repwd and repwd is not None:
            self.error_dict['repassword'] = "两次密码不一致"

    def check_email(self, email):
        print(email)
        if not match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            self.error_dict['email'] = "必填项：请确保你的邮箱是合法"
        elif UserInfo.objects.filter(email=email):
            self.error_dict['email'] = "邮箱已存在"

    def check_phone(self, phone):
        if not match(r"^1[35678]\d{9}$", phone):
            self.error_dict['phone'] = "必填项：请确保你的手机号合法"
        elif UserInfo.objects.filter(phone=phone):
            self.error_dict['phone'] = '手机号已注册，请直接登陆'

    def clean_data(self):
        """
        反射 执行每个字段的校验，并将错误信息写入error_list中
        :return: self.error_list
        """
        for key in self.data:
            if hasattr(self, 'check_{}'.format(key)):
                func = getattr(self, 'check_{}'.format(key))
                try:
                    func(*self.data.get(key))

                except Exception as e:
                    self.error_dict[key] = "数据不合法"
                    print(e)   #TODO：应该 写入日志

            self.data[key] = self.data.get(key)[0]

        return self.error_dict


def login(request):

    if request.method == "POST":
        check_data = CheckData(args_list=['username','password'] ,**request.POST)
        error_dict = check_data.clean_data()
        if not len(error_dict):

            username = request.POST.get('username')
            password = request.POST.get('password')

            if UserInfo.objects.filter(username=username).first().is_active:
                user = auth.authenticate(username=username,
                                         password=password)

                if user:
                    auth.login(request, user)
                    return redirect(reverse('blog:category_list', kwargs={'category_id': 1}))
            else:
                error_dict['active'] = "未激活的账户，请激活后登陆"

    return render(request, 'user/login.html')


def regist(request):
    error_dict = {}
    if request.method == "POST":
        check = CheckData(args_list=['username', 'password','email','phone','nickname','avatar'],**request.POST)
        error_dict = check.error_dict

        if not error_dict:
                user = UserInfo.objects.create_user(**check.data)

                # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
                # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密
                # 加密用户的身份信息，生成激活token
                serializer = Serializer(settings.SECRET_KEY, 3600)
                info = {'confirm': user.id}
                token = serializer.dumps(info)  # bytes
                token = token.decode()
                # 发邮件
                send_register_active_email.delay(user.email, user.username, token)
                return redirect(reverse('user:login'))

    return render(request, './user/regist.html', context={'error_dict':error_dict})
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
        user = UserInfo.objects.filter(id=user_id).first()
        user.is_active = 1
        user.save()

        # 跳转到登录页面
        return redirect(reverse('user:login'))
    except SignatureExpired as e:
        # 激活链接已过期
        return HttpResponse('激活链接已过期')


@login_required()
def logout(request):
    auth.logout(request)
    request.session.flush()


@login_required()
def resetpwd(request):
    if request.method == "POST":
        check = CheckData(args_list=['password', 'email'] ,**request.POST)
        error_dict = check.error_dict
        print(error_dict)
        if not error_dict:
            user = request.user
            user.set_password(request.POST.get('password'))
            user.save()
            return HttpResponse("reset password ok")

    return render(request, './user/resetpwd.html')


