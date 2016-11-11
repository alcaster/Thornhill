DEBUG = True
SECRET_KEY = 'e+31f+4nv8by4((7ivu8otd(@i0bn_07rzqz%51r28z@+za&nv'


ALLOWED_HOSTS = ['localhost', '127.0.0.1' , '192.168.1.79']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WSGI_APPLICATION = 'Thornhill.wsgi.application'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
