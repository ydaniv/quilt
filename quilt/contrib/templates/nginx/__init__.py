config = """# Generated by Quilt at ${timestamp}
# Nginx configuration for ${project_name}

user ${proxy_user}; # www-data
worker_processes ${proxy_workers}; # 4
pid /run/nginx.pid;

events {
    worker_connections ${proxy_worker_connections}; # 1024
    # multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;
    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log ${proxy_accesslog};
    error_log ${proxy_errorlog};
    gzip on;
    gzip_disable "msie6";
    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    upstream ${project_name} {
        server    ${app_location}:${app_port} fail_timeout=0;
    }

    # HTTPS ONLY REDIRECTS
    # server {
    #     listen *:80;
    #     server_name ${domain_names} ${machine_location};
    #     return 301 ${connection_scheme}${default_redirect_host}$request_uri;
    # }

    # server {
    #     listen      *:${machine_port};
    #     server_name ${hosts_to_redirect} ${machine_location};
    #     return 301 ${connection_scheme}${default_redirect_host}$request_uri;
    # }
    # END HTTPS ONLY REDIRECTS

    server {
        listen                      ${machine_port} default deferred; # ssl # HTTPS ONLY
        server_name                 ${domain_names};
        root                        ${project_root};
        keepalive_timeout           5;
        large_client_header_buffers 4 256k;
        client_max_body_size        4G;

        # HTTPS ONLY
        # ssl_certificate           /srv/ssl/${ssl_certificate_name};
        # ssl_certificate_key       /srv/ssl/${ssl_certificate_key_name};
        # ssl_protocols             TLSv1 TLSv1.1 TLSv1.2;
        # ssl_ciphers               ECDHE-RSA-AES256-SHA384:AES256-SHA256:RC4:HIGH:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!AESGCM;
        # ssl_prefer_server_ciphers on;
        # ssl_session_cache         shared:SSL:10m;
        # ssl_session_timeout       10m;

        location /static/ {

        }

        location / {
            client_max_body_size    10m;
            client_body_buffer_size 256k;

            proxy_buffer_size       256k;
            proxy_buffers           4 256k;
            proxy_busy_buffers_size 256k;

            proxy_connect_timeout   90;
            proxy_send_timeout      90;
            proxy_read_timeout      90;

            proxy_set_header        X-Forwarded-Proto $scheme;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header        X-Real-IP $remote_addr;
            proxy_set_header        Host $http_host;
            proxy_redirect          off;
            proxy_pass              http://${project_name};
        }
}
"""


supervisor = """

"""