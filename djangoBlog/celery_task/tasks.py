from django.core.mail import send_mail
from djangoBlog.settings import develop
from celery import Celery


# 在任务处理者一端加这几句
import os
import django

PROFILE_LIST = {1: 'develop',
                2: 'product'}

profile = os.environ.get('PROJECT_PROFILE', PROFILE_LIST.get(1,2))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','djangoBlog.settings.{}'.format(profile))
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):

    from django.core.urlresolvers import reverse

    URL = 'http://127.0.0.1:8000{}'.format(reverse('user:active', kwargs={'token': token}))
    subject = '欢迎注册 Monkey Blog!'
    message = 'join us！'
    sender = develop.EMAIL_FROM
    receiver = [to_email]
    html_message = """{}:<br><p style="text-indent: 32px">亲爱的 {} 终于等到你！欢迎注册 Monkey Blog ～ ！加入我们，让生活有 <span style="color: #3b9a7c">技</span> 循。</p><p><a href="{}">点击激活您的账户！</a><br>{}<br></p><p style="margin-top: 160px; text-align: right">——Monkey Blog 项目组！</p>
""".format(username, username, URL, URL)

    send_mail(subject, message, sender, receiver, html_message=html_message)
