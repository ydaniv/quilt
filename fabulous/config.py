import datetime
from fabric.api import env
from fabric.contrib import django
from django.conf import settings as django_settings


env.use_ssh_config = True
env.forward_agent = True
env.user = 'robot'
env.roledefs = {'web': ['']}


CONFIG = {

    'timestamp': datetime.datetime.now(),
    'user': env.user,
    'password': '',

    'machine': {
        # ubuntu
        'location': env.roledefs['web'][0],
        'port': 80,
    },

    'project': {
        # django
        'name': '',
        'root': '',
        'env': '',
        'allowed_hosts': [],
        'cookie_domain': '',
        'initial_data': {
            'local': [],
            'remote': [],
        },
        'secret_key': '',
    },

    'app': {
        # gunicorn
        'location': '127.0.0.1',
        'port': 9000,
        'workers': 4,
        'timeout': 30,
        'wsgi': '',
        'access_log': '',
        'error_log': ''
    },

    'db': {
        # postgres
        'user': env.user,
        'name': '',
        'password': '',
        'dump_file': '',
    },

    'q': {
        # celery
        'location': '127.0.0.1',
        'port': 9000,
        'workers': 4,
        'timeout': 30,
        'access_log': '',
        'error_log': ''
    },

    'cache': {
        # redis
        'access_log': '',
        'error_log': '',
    },

    'proxy': {
        # nginx
        'access_log': '',
        'error_log': '',
    },

    'email': {
        'user': '',
        'password': '',
    },

    'repository': {
        'location': '',
        'branch': 'develop',
    },

    'services': {
        'sentry_dsn': '',
    },

}

CONFIG.update(django_settings.FABULOUS)

WORKON = 'workon ' + CONFIG['project_name']

DEACTIVATE = 'deactivate'
