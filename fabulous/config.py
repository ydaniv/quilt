import datetime
from fabric.api import env
from fabfile import config


env.use_ssh_config = True
env.forward_agent = True
env.user = 'robot'
env.roledefs = {'web': ['']}


CONFIG = {
    'timestamp': datetime.datetime.now(),
    'user': env.user,

    # machine
    'machine_location': env.roledefs['web'][0],
    'machine_port': 80,

    # project
    'project_name': '',
    'project_root': '',
    'project_env': '',
    'project_initial_data': {
        'local': [],
        'remote': [],
    },
    'project_allowed_hosts': [''],
    'project_cookie_domain': '',
    'project_secret_key': '',

    # app server
    'app_location': '127.0.0.1',
    'app_port': 9000,
    'app_workers': 4,
    'app_timeout': 30,
    'app_wsgi': '',

    'q_workers': 2,
    'q_max_tasks_per_child': '',

    # db server
    'db_name': '',
    'db_user': env.user,
    'db_password': '',
    'db_dump_file': '',

    # cache server
    # any redis settings here

    # email server
    'email_user': '',
    'email_password': '',

    # code repository
    'repository_location': '',
    'repository_branch': 'develop',

    # services
    'sentry_dsn': '',

    # logs
    'proxy_access_log': '/srv/logs/proxy_access.log',
    'proxy_error_log': '/srv/logs/proxy_error.log',
    'app_access_log': '/srv/logs/app_access.log',
    'app_error_log': '/srv/logs/app_access.log',
    'q_access_log': '/srv/logs/q_access.log',
    'cache_access_log': '/srv/logs/cache_access.log',
    'cache_error_log': '/srv/logs/cache_error.log',

}


CONFIG.update(config.FABULOUS)

WORKON = 'workon ' + CONFIG['project_name']

DEACTIVATE = 'deactivate'
