import os

HOST = 'blackmonkey.cn'

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

ADMINS = MANAGERS = ('root:monkey', '931976722@qq.com')

ALLOWED_HOSTS = ['*']

REDIS_URL = "redis://127.0.0.1:6379/1"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            # 'PASSWORD': '',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool'
    }
}

LOGGER_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

LOGGER_DIR_NAME = 'log'

LOGGER_PATH = os.path.join(LOGGER_BASE_DIR, LOGGER_DIR_NAME, 'djangoblog.log')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s:'
                      '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGER_PATH,
            'formatter': 'default',
            'maxBytes': 1024 * 1024,  # 1M
            'backupCount': 5,
        },

    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
