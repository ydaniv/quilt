proxy = """### Generated via Fabric on ${timestamp}
# nginx configuration for ${project_name}

upstream ${project_name} {
    server    ${app_location}:${app_port};
}

server {
    listen      *:${machine_port};
    server_name ${domain_names};
    root                 ${project_root};
    access_log           ${log_proxy_access};
    error_log            ${log_proxy_error};

    location /static/ {

    }

    location / {
        proxy_pass              http://${project_name};
        proxy_redirect          off;
        proxy_set_header        Host            $$host;
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


app = """### Generated via Fabric on ${timestamp}
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

exec ${app_cmd_prefix} ${project_env}/bin/gunicorn ${app_wsgi} --bind ${app_location}:${app_port} --workers ${app_workers} --timeout ${app_timeout} --access-logfile ${log_app_access} --error-logfile ${log_app_error}
"""


queue = """### Generated via Fabric on ${timestamp}
# rq configuration for ${project_name}

author "${user}"
description "Controls rq for ${project_name}"

start on starting ${project_name}
stop on stopping ${project_name}
respawn
console log
setuid ${user}
setgid ${user}
chdir ${project_root}

exec ${project_env}/bin/python manage.py rqworker default

"""
