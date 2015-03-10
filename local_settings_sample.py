import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'putsomethingreallycoolhere'

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.db'),
    }
}

TIME_ZONE = 'America/Denver'
