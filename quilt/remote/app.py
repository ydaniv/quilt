import cuisine
from fabric.api import env, task, roles, sudo
from quilt import utilities, contrib


@roles('app')
@task
def ensure():
    utilities.notify(u'Configuring gunicorn.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.app, context)
    cuisine.file_write('/etc/init/' + env.project_name + '.conf', content)
    restart()


@roles('app')
@task
def start():
    utilities.notify(u'Starting the app server.')

    sudo('service ' + env.project_name + ' start')


@roles('app')
@task
def stop():
    utilities.notify(u'Stopping the app server.')

    sudo('service ' + env.project_name + ' stop')


@roles('app')
@task
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service ' + env.project_name + ' restart')
