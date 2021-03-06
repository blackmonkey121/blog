import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fbm_@40m#ljf$+^vy-u_z7ppow4@l8$d7zk5!_ngj#!nt@)k^s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [

    'gunicorn',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'xadmin',
    'crispy_forms',

    'apps.blog.apps.BlogConfig',
    'apps.user.apps.UserConfig',
    'apps.config.apps.ConfigConfig',
    'apps.comment.apps.CommentConfig',

    'ckeditor',
    'ckeditor_uploader',   # 添加文件支持
    'rest_framework',
    'dal',
    'dal_select2',  # autocomplete
]

MIDDLEWARE = [
    'apps.blog.middleware.user_id.UserIDMiddleware',
    'apps.blog.middleware.user_id.GetUserMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoBlog.urls'

##########################################################
# 主题名
# 只需修改这个变量 就会整体应用整个样式
THEME_NAME = 'default'   # milk / black

# 主题文件路径
THEME_URL = os.path.join(BASE_DIR, 'themes', THEME_NAME)

##########################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(THEME_URL, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT  = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

THEME_STATIC = 'default'

STATICFILES_DIRS = [
    os.path.join(THEME_URL, 'static'),
]

AUTH_USER_MODEL = 'user.UserInfo'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/user/login/'

XADMIN_TITLE = "Monkey Blog 管理后台"

XADMIN_FOOTER_TITLE = "Power by monkey.com"

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# smtp服务地址
EMAIL_HOST = 'smtp.qq.com'

# SMTP端口 25 服务器开放
EMAIL_PORT = 25

# 发送邮件的邮箱
EMAIL_HOST_USER = '3213322480@qq.com'

# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxx'

# 收件人看到的发件人
EMAIL_FROM = 'MonkeyBlog <3213322480@qq.com>'

EMIAL_USE_TLS = False

# ckeditor settings
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 700,
        'width': 800,
        'tabSpaces': 3,
        'extraPlugins': 'codesnippet',   # 配置代码插件
    }
}

# CKeditor static settings
CKEDITOR_UPLOAD_PATH = 'article_upload/'

DEFAULT_FILE_STORAGE = 'libs.storage.WatermarkStorage'

# rest-framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',   #
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',   # 分页
    'PAGE_SIZE': 5
}

AUTHENTICATION_BACKENDS = [
    'libs.login_tools.CustomBackend',
]

if DEBUG:
    from .develop import *
else:
    from .product import *

