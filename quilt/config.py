import datetime
from fabric.api import env


QUILT = {

    'timestamp': datetime.datetime.now(),

    # fabric
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
    'initial_data': ['local/sites'],
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

    # queue server
    'queue_workers': 2,

    # db server
    'db_name': '',
    'db_user': 'robot',
    'db_password': '',
    'db_dump_file': '/dump_{timestamp}.sql'.format(timestamp=datetime.datetime.now()),

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
    'log_proxy_access': '',
    'log_proxy_error': '',
    'log_app_access': '',
    'log_app_error': '',
    'log_queue_access': '',
    'log_cache_access': '',
    'log_cache_error': '',

}

env.update(QUILT)