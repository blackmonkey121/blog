from .base import *    # No Q/A
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoBlog',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'monkey123',
    }
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# smtp服务地址
EMAIL_HOST = 'smtp.qq.com'

# SMTP端口 25 服务器开放
EMAIL_PORT = 25

# 发送邮件的邮箱
EMAIL_HOST_USER = '3213322480@qq.com'

# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'yyuylfcxyzjfdgea'

# 收件人看到的发件人
EMAIL_FROM = 'MonkeyBlog <3213322480@qq.com>'


# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 2
# SESSION_REDIS_PASSWORD = ''
# SESSION_REDIS_PREFIX = 'session'
