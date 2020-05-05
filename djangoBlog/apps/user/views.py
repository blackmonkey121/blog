from django.http import JsonResponse
from django.shortcuts import redirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.views import View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Group  # 权限分类注册

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired

from celery_task.tasks import send_register_active_email, send_update_pwd_email
from .user_forms import LoginForm, RegistForm, UpdateForm, ResetForm
from .models import UserInfo
from libs.login_tools import authenticate


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
            token = self.serializer.dumps(info)  # bytes
            token = token.decode()
            return token
        raise (ValueError, _("user is not exists!"))

    def load_token(self, token):
        """
        :param token: 接受包含用户信息的token
        :return: 返回用户对象
        """
        info = self.serializer.loads(token)

        # 获取改密用户对象
        user_id = info['user_id']
        user = UserInfo.objects.filter(id=user_id).first()
        return user

    def get_user(self, email):
        user = UserInfo.objects.filter(email=email).first()
        return user


class SendEmailMixin(Token):

    def send_active(self, user):
        token = self.dump_token(user=user)
        email = user.email
        send_register_active_email.delay(to_email=email, username=user.username, token=token)

    def send_update(self):
        pass


class LoginView(FormView):
    def __init__(self):
        self.ret = {'status': None, 'msg': None}
        super(LoginView, self).__init__()

    template_name = 'user/login.html'

    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_check:
            return redirect(reverse('index'))
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        # 自定义的 authenticate

        user = authenticate(self.request, username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password'))
        if user:
            if user.is_check:

                auth.login(self.request, user)
                self.ret['status'] = True
                self.ret['msg'] = reverse('index')
                print('ok')
            else:
                self.ret['msg'] = {"username": "账号尚未激活"}
                self.ret["check"] = True
                print('no login')
        else:
            self.ret['msg'] = {'password': '账号或密码不正确'}
            print('msg error')

        ret = JsonResponse(self.ret)
        if self.request.user.username:
            ret.set_cookie('user', hash(user.id), max_age=60 * 60 * 24 * 7)

        return ret

    def form_invalid(self, form):
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
        ret = redirect(reverse('user:login'))
        ret.delete_cookie('user')
        return ret


class RegistView(CreateView, SendEmailMixin):
    def __init__(self):
        self.ret = {"status": None, "msg": None}
        super(RegistView, self).__init__()

    model = UserInfo

    form_class = RegistForm

    template_name = 'user/regist.html'

    def form_valid(self, form):
        form.cleaned_data.pop("repassword")
        # 发送邮件

        user = UserInfo.objects.create_user(**form.cleaned_data, is_staff=True)
        user.groups.add(1)

        self.send_active(user=user)
        self.ret["status"] = True
        self.ret["msg"] = {"email": user.email, 'url': reverse('user:login')}

        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret["msg"] = form.errors
        return JsonResponse(self.ret)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'url': reverse('user:regist')})
        return context


class UpdatePassWordView(FormView, Token):
    def __init__(self):
        self.ret = {'status': None, 'msg': {}}
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
        self.ret['msg'].update({'email': email, })
        if user:
            token = self.dump_token(user=user)
            send_update_pwd_email.delay(email, user.username, token)
            self.ret["status"] = True
            self.ret["msg"].update({'url': reverse('user:login')})
        else:
            self.ret['msg'].update({'url': reverse('user:regist'), })
        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret['msg'] = form.errors
        return JsonResponse(self.ret)

    def render_to_response(self, context, **response_kwargs):
        context.update({"key": "提交修改"})
        return super().render_to_response(context, **response_kwargs)


class ResetView(UpdateView, Token):
    def __init__(self):
        self.ret = {"status": None, "msg": {}}
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
            self.ret['msg'] = {"new_re_password": "激活链接已过期"}
            # 激活链接已过期
            return JsonResponse(self.ret)

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_re_password')
        self.object.set_password(new_password)
        self.object.save()
        self.ret["status"] = True
        self.ret['msg'].update({'url': reverse("user:login")})
        return JsonResponse(self.ret)

    def form_invalid(self, form):
        self.ret["msg"] = form.errors
        return JsonResponse(self.ret)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content.update({"key": "重置密码"})
        return content


class ActiveView(FormView, Token):

    def dispatch(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        try:
            user = self.load_token(token=token)
            user.is_check = True
            user.save()
            return HttpResponse("您的账户已激活,<a href='{}'>Go Login</a>".format(reverse('user:login')))

        except Exception as e:
            return HttpResponse("出了一些状况，稍后再试！")

    def get_form(self, form_class=None):
        pass


