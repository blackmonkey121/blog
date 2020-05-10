from django.core.mail import send_mail
from djangoBlog.settings import setting
from celery import Celery

# 在任务处理者一端加这几句
import os
import django
from django.urls import reverse

# HOST = 'www.xxxxxxx.cn'
HOST = '127.0.0.1:8000'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBlog.settings.setting')
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_bar.tasks', broker='redis://127.0.0.1:6379/0')


# 定义任务函数
@app.task(bind=True, max_retries=3,default_retry_delay=1 * 6)
def send_register_active_email(self, to_email, username, token):
    URL = 'http://{}{}'.format(HOST, reverse('user:active', kwargs={'token': token}))
    subject = '欢迎注册 MonkeyBlog!'
    message = 'Join Us！'
    sender = setting.EMAIL_FROM
    receiver = [to_email]
    html_message = """{}:<br><p style="text-indent: 32px">亲爱的 {} 终于等到你！欢迎注册 MonkeyBlog ～ ！</p><p><a href="{}">点击激活您的账户！</a><br>{}<br></p><p style="margin-top: 160px; text-align: right">——MonkeyBlog 项目组！</p>
""".format(username, username, URL, URL)
    try:
        send_mail(subject, message, sender, receiver, html_message=html_message)
    except Exception as e:
        print(e)

@app.task(bind=True, max_retries=3,default_retry_delay=1 * 6)
def send_update_pwd_email(self, to_email, username, token):
    URL = 'http://{}{}'.format(HOST, reverse('user:reset', kwargs={'token': token}))
    subject = '密码重置提示 确认邮件!'
    message = '您的密码重置申请已通过，点击下方链接进行修改'
    sender = setting.EMAIL_FROM
    receiver = [to_email]
    html_message = """{}:<br><p style="text-indent: 32px">{} 这是修改密码的验证链接，如果是你的操作，请点击下面的链接修改密码，如果不是，可能您的账户存在安全风险，请主动修改密码。</p><p> 链接:<a href="{}"> </a><br>{}<br></p><p style="margin-top: 160px; text-align: right">——MonkeyBlog 项目组！</p>
""".format(username, username, URL, URL)
    try:
        send_mail(subject, message, sender, receiver, html_message=html_message)
    except Exception as e:
        print(e)
# TODO:实现用户统计。应该异步的来做，以节省开支和每次浏览对数据的写操作。将这些事情交给 celery
