from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views import View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired

from celery_task.tasks import send_register_active_email, send_update_pwd_email
from .user_forms import LoginForm, RegistForm, UpdateForm, ResetForm
from .models import UserInfo

class Token(object):
    serializer = Serializer(settings.SECRET_KEY, 3600)

    def create_serializer(self, SECRET_KEY, LIMIT_TIME):
        self.__class__.serializer = Serializer(SECRET_KEY, LIMIT_TIME)

    def dump_token(self, user):
        """
        接受用户对象，返回包含用户id 的 token 信息
        :param user: 用户对象
        :return: token
        """
        if isinstance(user, UserInfo):

            info = {'user_id': user.id}
            print(info)
            token = self.serializer.dumps(info)  # bytes
            token = token.decode()
            return token
        raise (ValueError, "user is not exists!")

    def load_token(self, token):
        """
        :param token: 接受包含用户信息的token
        :return: 返回用户对象
        """
        info = self.serializer.loads(token)
        print(info)
        # 获取改密用户对象
        user_id = info['user_id']
        user = UserInfo.objects.filter(id=user_id).first()
        return user

    def get_user(self,email):
        user = UserInfo.objects.filter(email=email).first()
        return user


def index(request):
    return render(request, 'user/index.html')


class LoginView(FormView):
    ret = {'status': True, 'msg': None}

    template_name = 'user/login.html'

    form_class = LoginForm

    success_url = reverse_lazy('user:home')  # 因为在文件导入时不加载 urls 必须使用lazy

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_check:
            return redirect(reverse('user:home'))
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        user = auth.authenticate(username=form.cleaned_data.get('username'),
                                 password=form.cleaned_data.get('password'))
        if user:
            if user.is_check:

                auth.login(self.request, user)
                self.ret['msg'] = reverse('user:home')
            else:
                self.ret['status'] = None
                self.ret['msg'] = {"username": "账号尚未激活,"}
        else:
            self.ret['status'] = None
            self.ret['msg'] = {'password': '账号或密码不正确！'}

        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret['status'] = None
        self.ret['msg'] = form.errors
        return JsonResponse(self.ret)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'url': reverse('user:login')})
        return context


class LogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        request.session.flush()
        return redirect(reverse('user:login'))


class RegistView(CreateView, Token):
    def __init__(self):
        self.ret = {"status": True, "msg": None}
        super(RegistView, self).__init__()

    model = UserInfo

    form_class = RegistForm

    template_name = 'user/regist.html'

    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        form.cleaned_data.pop("repassword")
        self.ret["msg"] = reverse('user:login')
        # 发送邮件
        # user = self.get_user(email)
        user = User(**form.cleaned_data)
        email = user.email
        token = self.dump_token(user=user)
        send_register_active_email(to_email=email, username=user.username, token=token)
        self.ret["msg"] = {"email": email}
        user.save()
        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret["msg"] = form.errors
        self.ret["status"] = 0
        return JsonResponse(self.ret)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'url': reverse('user:regist')})
        return context


class UpdatePassWordView(FormView, Token):
    def __init__(self):
        self.ret = {'status': True, 'msg': {}}
        super(UpdatePassWordView, self).__init__()

    template_name = 'user/update.html'

    model = UserInfo

    form_class = UpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'url': reverse('user:update')})
        return context

    def form_valid(self, form):

        # 发邮件
        email = form.cleaned_data.get('email')
        user = self.get_user(email)
        self.ret['msg'].update({'email': email,})
        if user:
            token = self.dump_token(user=user)
            send_update_pwd_email.delay(email, user.username, token)
            self.ret["msg"].update({'url': reverse('user:login')})
        else:
            self.ret["status"] = None
            self.ret['msg'].update({'url': reverse('user:regist'), })
        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret['status'] = None
        self.ret['msg'] = form.errors
        return JsonResponse(self.ret)

    def render_to_response(self, context, **response_kwargs):
        context.update({"key": "提交修改"})
        return super().render_to_response(context, **response_kwargs)


class ResetView(UpdateView, Token):
    def __init__(self):
        self.ret = {"status": True, "msg": {}}
        super().__init__()

    model = UserInfo

    form_class = ResetForm

    template_name = 'user/update.html'

    def get_object(self, queryset=None):
        try:
            token = self.kwargs.get('token')
            user = self.load_token(token=token)
            return user

        except SignatureExpired as e:
            self.ret['status'] = None
            self.ret['msg'] = {"new_re_password":"激活链接已过期"}
            # 激活链接已过期
            return JsonResponse(self.ret)

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_re_password')
        self.object.set_password(new_password)
        self.object.save()
        self.ret['msg'].update({'url': reverse("user:login")})
        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret["status"] = None
        self.ret["msg"] = form.errors
        return JsonResponse(self.ret)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content.update({"key": "重置密码"})
        return content


class ActiveView(View, Token):
    ret = {"status": True, 'msg':None}
    def dispatch(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        try:
            user = self.load_token(token=token)
            user.is_check = True
            user.save()
        except Exception as e:
            self.ret['status'] = False
        return JsonResponse(self.ret)