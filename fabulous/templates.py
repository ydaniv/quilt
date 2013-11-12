nginx = """### Generated via Fabric on ${timestamp}
# nginx configuration for ${project_name}

upstream ${project_name} {
    server    ${app_location}:${app_port};
}

server {
    listen      *:${machine_port};
    server_name ${domain_names};
    root                 ${project_root};
    access_log           ${proxy_access_log};
    error_log            ${proxy_error_log};

    location /static/ {

    }

    location / {
        proxy_pass              http://${project_name};
        proxy_redirect          off;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size    10m;
        client_body_buffer_size 128k;
        proxy_connect_timeout   90;
        proxy_send_timeout      90;
        proxy_read_timeout      90;
        proxy_buffers           32 4k;
    }
}
"""


gunicorn = """### Generated via Fabric on ${timestamp}
# gunicorn upstart configuration for ${project_name}

author "${user}"
description "Controls Gunicorn for ${project_name}"

start on (filesystem)
stop on runlevel [016]
respawn
console log
setuid ${user}
setgid ${user}
chdir ${project_root}

exec ${project_env}/bin/gunicorn ${app_wsgi} --bind ${app_location}:${app_port} --workers ${app_workers} --timeout ${app_timeout} --access-logfile ${app_access_log} --error-logfile ${app_error_log}
"""


celery = """### Generated via Fabric on ${timestamp}
# celery configuration for ${project_name}

author "${user}"
description "Controls Celery for ${project_name}"

start on starting ${project_name}
stop on stopping ${project_name}
respawn
console log
setuid ${user}
setgid ${user}
chdir ${project_root}

exec ${project_env}/bin/python manage.py celery worker --concurrency=${q_workers} --maxtasksperchild=${q_max_tasks_per_child} --logfile=${q_access_log}

"""


production_settings = """### Generated via Fabric on ${timestamp}
from ${project_name}.settings import *


ALLOWED_HOSTS = ${project_allowed_hosts}

SESSION_COOKIE_DOMAIN = '${project_cookie_domain}'

SENTRY_DSN = '${sentry_dsn}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_user}',
        'PASSWORD': '${db_password}',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

"""
