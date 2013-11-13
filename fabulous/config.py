import datetime
from fabric.api import env, local


FABULOUS_DEFAULT = {

    'timestamp': datetime.datetime.now(),
    'runner': local,

    # fabric env
    'user': 'robot',
    'password': '',
    'key_filename': '',
    'roledefs': {'local': ['127.0.0.1']},
    'roles': ['local'],
    'use_ssh_config': True,
    'forward_agent': True,

    # machine
    'machine_location': '127.0.0.1',
    'machine_port': 8000,

    # virtualenv
    'workon': '',
    'deactivate': 'deactivate',

    # project
    'project_name': '',
    'project_root': '',
    'project_env': '',
    'initial_data': [''],
    'project_allowed_hosts': [''],
    'project_cookie_domain': '',
    'secret_key': '',
    'target_settings_template': '',
    'target_settings_destination': '',

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
    'db_user': '',
    'db_password': '',
    'db_dump_file': '',

    # cache server
    # any redis settings here

    # email server
    'email_user': '',
    'email_password': '',

    # code repository
    'repository_location': '',
    'repository_work_branch': 'develop',
    'repository_deploy_branch': 'master',

    # services
    'sentry_dsn': '',

    # logs
    'log_proxy_access': '/srv/logs/proxy_access.log',
    'log_proxy_error': '/srv/logs/proxy_error.log',
    'log_app_access': '/srv/logs/app_access.log',
    'log_app_error': '/srv/logs/app_access.log',
    'log_q_access': '/srv/logs/q_access.log',
    'log_cache_access': '/srv/logs/cache_access.log',
    'log_cache_error': '/srv/logs/cache_error.log',

}
