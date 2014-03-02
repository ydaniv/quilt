import cuisine
from fabric.api import env, task, roles, sudo, execute
from quilt import utilities, contrib


@roles('proxy')
@task
def ensure():
    utilities.notify(u'Configuring the proxy server.')

    context = env
    context.update({'domain_names': ' '.join(env.project_allowed_hosts)})
    cuisine.mode_sudo()
    content = cuisine.text_template(env.proxy_config_template, context)
    cuisine.file_write(env.proxy_config_file, content)
    execute(restart)


@roles('proxy')
@task
def start():
    utilities.notify(u'Starting the proxy server.')

    sudo(env.proxy_command_start)


@roles('proxy')
@task
def stop():
    utilities.notify(u'Stopping the proxy server.')

    sudo(env.proxy_command_stop)


@roles('proxy')
@task
def restart():
    utilities.notify(u'Restarting the proxy server.')

    sudo(env.proxy_command_restart)
