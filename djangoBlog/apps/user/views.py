from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from .models import UserInfo
from django.conf import settings
from celery import Celery
from celery_task.tasks import send_register_active_email,send_getpwd_email
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
            pass
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


def login(request):
    if request.user.username:
        return redirect(reverse('index'))

    ret_msg = {'status': 0, 'msg': {}}
    if request.method == "POST":
        check = CheckData(args_list=['username', 'password'], **request.POST)
        check.clean_data()
        if not check.error_dict:
            check.data.pop('save')
            user = auth.authenticate(**check.data)
            if user:
                if not user.is_check:
                    ret_msg["msg"]["username"] = "账户未激活 email:{}".format(user.email)
                else:
                    auth.login(request, user)
                    ret_msg["status"] = 1
                    ret_msg["msg"] = reverse('blog:home', kwargs={"user_id": user.id})
            else:
                ret_msg["msg"]["password"] = "用户名或密码不正确。"

        else:
            ret_msg['msg'] = check.error_dict
        return JsonResponse(ret_msg)
    return render(request, 'user/login.html')


def regist(request):
    ret_msg = {'status': 0, 'msg': {}}
    if request.method == "POST":
        # 数据检验
        avatar = [request.FILES.get('avatar'),]
        data = request.POST.copy()
        try:
            data.pop('avatar')
        except Exception as e:
            print(e)
        check = CheckData(args_list=['username', 'password','email','phone','nickname'],**data, avatar=avatar)
        check.clean_data()

        # 用户名唯一 校验
        if UserInfo.objects.filter(username=request.POST.get('username')):
            check.error_dict["username"] = "用户名已被注册，换一个吧！"

        if not check.error_dict:

            ret_msg['status'] = 1
            ret_msg['msg'] = reverse('user:login')
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
        else:
            ret_msg['msg'] = check.error_dict

        return JsonResponse(ret_msg)

    return render(request, './user/regist.html')


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
        user.is_check = True
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
    return HttpResponse('')


@login_required()
def resetpwd(request):
    ret_msg = {"status": 0, "msg": {}}
    if request.method == "POST":
        # 重写 验证类的邮箱验证方法
        class myCheckData(CheckData):
            def check_email(self, email):
                if not match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
                    self.error_dict['email'] = "必填项：请确保你的邮箱是合法"

        check = myCheckData(args_list=['password', 'email'] ,**request.POST)
        check.clean_data()
        user = request.user

        if user.email != request.POST.get('email'):
            check.error_dict['email'] = "邮箱错误，查验后再试！"

        if not check.error_dict:
            user.set_password(request.POST.get('password'))
            user.save()
            ret_msg['status'] = 1
            ret_msg['msg'] = "修改密码成功！"
            return JsonResponse(ret_msg)

        ret_msg['msg'] = check.error_dict
        return JsonResponse(ret_msg)

    return render(request, './user/resetpwd.html')


def forgetpwd(request):
    ret_msg = {"status": 0, "msg": {}}
    if request.method == "POST":

        # 重写 验证类的邮箱验证方法
        class myCheckData(CheckData):
            def check_email(self, email):
                if not match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
                    self.error_dict['email'] = "必填项：请确保你的邮箱是合法"

        check = myCheckData(args_list=['email'], **request.POST)
        check.clean_data()

        # 检查邮箱是否注册 注册拿到用户 没注册 写入错误信息
        if not check.error_dict:
            email = request.POST.get('email')
            user = UserInfo.objects.filter(email=email).first()

            if user:
                serializer = Serializer(settings.SECRET_KEY, 3600)
                info = {'confirm': user.id}
                token = serializer.dumps(info)  # bytes
                token = token.decode()
                # 发邮件
                send_getpwd_email.delay(email, user.username, token)

                ret_msg['status'] = 1
                ret_msg['msg'] = "验证邮件已发送，请前往{}查验".format(email)
                return JsonResponse(ret_msg)
            else:
                check.error_dict['email'] = "此邮箱尚未注册！"

        ret_msg['msg'] = check.error_dict
        return JsonResponse(ret_msg)

    return render(request, './user/forgetpwd.html')

def pwdreset(request, token):

    ret_msg = {'status': 0, 'msg': {}}
    serializer = Serializer(settings.SECRET_KEY, 3600)
    if request.method == "POST":
        user_id = request.COOKIES.get('repwd_user_id')
        if user_id:
            check = CheckData(args_list=['password'], **request.POST)
            check.clean_data()

            if not check.error_dict:
                user_id = request.COOKIES.get('repwd_user_id')
                user = UserInfo.objects.filter(id=user_id).first()
                password = request.POST.get("password")
                user.set_password(password)
                user.save()
                ret_msg['status'] = 1

            ret_msg['msg'] = check.error_dict
        ret_msg['msg'] = '改密链接失效！'
        return JsonResponse(ret_msg)

    try:
        info = serializer.loads(token)
        user_id = info['confirm']
        # 根据id获取用户信息
        user = UserInfo.objects.filter(id=user_id).first()
        if user:
            response = HttpResponse(render(request,'user/pwdreset.html'))
            response.set_cookie('repwd_user_id',user_id,max_age=60*10)

            return response

    except SignatureExpired as e:
        # 激活链接已过期
        return HttpResponse('激活链接已过期')
