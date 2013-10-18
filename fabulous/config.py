import datetime
from fabric.api import env
from fabric.contrib import django
#django.project('')
#from django.conf import settings


env.use_ssh_config = True
env.forward_agent = True
env.user = ''
env.roledefs = {'web': ['']}

CONFIG = {
    'sentry_dsn': '',
    'user': env.user,
    'machine_location': env.roledefs['web'][0],
    'machine_port': 80,
    'project_name': '',
    'project_root': '',
    'project_env': '',
    'db_name': '',
    'db_user': env.user,
    'db_dump_file': '',
    'dataset_root': '',
    'dataset_repo': '',
    'dataset_branch': '',
    'app_location': '127.0.0.1',
    'app_port': 9000,
    'app_workers': 4,
    'app_timeout': 30,
    'app_wsgi': '',
    'repo': '',
    'branch': '',
    'allowed_hosts': [''],
    'cookie_domain': '',
    'nginx_access_log': '',
    'nginx_error_log': '',
    'gunicorn_access_log': '',
    'gunicorn_error_log': '',
    'redis_access_log': '',
    'redis_error_log': '',
    'timestamp': datetime.datetime.now(),
}

WORKON = 'workon ' + CONFIG['project_name']

DEACTIVATE = 'deactivate'
