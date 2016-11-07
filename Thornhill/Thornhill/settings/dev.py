DEBUG = True
SECRET_KEY = 'e+31f+4nv8by4((7ivu8otd(@i0bn_07rzqz%51r28z@+za&nv'


ALLOWED_HOSTS = ['localhost', '127.0.0.1' , '192.168.1.79']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WSGI_APPLICATION = 'Thornhill.wsgi.application'
