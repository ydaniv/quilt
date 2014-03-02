import cuisine
from fabric.api import env, task, roles, sudo
from quilt import utilities, contrib


@roles('app')
@task
def ensure():
    utilities.notify(u'Configuring gunicorn.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.app_config_template, context)
    cuisine.file_write(env.app_config_file, content)
    restart()


@roles('app')
@task
def start():
    utilities.notify(u'Starting the app server.')

    sudo(env.app_command_start)


@roles('app')
@task
def stop():
    utilities.notify(u'Stopping the app server.')

    sudo(env.app_command_stop)


@roles('app')
@task
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo(env.app_command_restart)
