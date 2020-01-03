from django.core.mail import send_mail
from djangoBlog.settings import develop
from apps.blog.models import Post
from celery import Celery

# 在任务处理者一端加这几句
import os
import django
from django.core.urlresolvers import reverse

PROFILE_LIST = {1: 'develop',
                2: 'product'}

profile = os.environ.get('PROJECT_PROFILE', PROFILE_LIST.get(1, 2))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBlog.settings.{}'.format(profile))
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    URL = 'http://127.0.0.1:8000{}'.format(reverse('user:active', kwargs={'token': token}))
    subject = '欢迎注册 Monkey Blog!'
    message = 'join us！'
    sender = develop.EMAIL_FROM
    receiver = [to_email]
    html_message = """{}:<br><p style="text-indent: 32px">亲爱的 {} 终于等到你！欢迎注册 Monkey Blog ～ ！加入我们，让生活有 <span style="color: #3b9a7c">技</span> 循。</p><p><a href="{}">点击激活您的账户！</a><br>{}<br></p><p style="margin-top: 160px; text-align: right">——Monkey Blog 项目组！</p>
""".format(username, username, URL, URL)

    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def send_getpwd_email(to_email, username, token):
    URL = 'http://127.0.0.1:8000{}'.format(reverse('user:pwdreset', kwargs={'token': token}))
    subject = '欢迎注册 Monkey Blog!'
    message = 'join us！'
    sender = develop.EMAIL_FROM
    receiver = [to_email]
    html_message = """{}:<br><p style="text-indent: 32px">{} 这是修改密码的验证链接，如果是你的操作，请点击下面的链接通过改密，如果不是，可能您的账户存在安全风险，请主动修改密码。</p><p><a href="{}">点击通过本次密码修改！</a><br>{}<br></p><p style="margin-top: 160px; text-align: right">——Monkey Blog 项目组！</p>
""".format(username, username, URL, URL)

    send_mail(subject, message, sender, receiver, html_message=html_message)

# TODO:实现用户统计。应该异步的来做，以节省开支和每次浏览对数据的写操作。将这些事情交给 celery