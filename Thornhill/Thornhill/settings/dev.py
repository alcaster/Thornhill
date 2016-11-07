DEBUG = True
SECRET_KEY = 'e+31f+4nv8by4((7ivu8otd(@i0bn_07rzqz%51r28z@+za&nv'




CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WSGI_APPLICATION = 'Thornhill.wsgi.application'
