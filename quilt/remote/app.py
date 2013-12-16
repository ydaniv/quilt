import cuisine
from fabric.api import env, task, sudo
from quilt import utilities, contrib


@task
def ensure():
    utilities.notify(u'Configuring gunicorn.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.app, context)
    cuisine.file_write('/etc/init/' + env.project_name + '.conf', content)
    restart()


@task
def start():
    utilities.notify(u'Starting the app server.')

    sudo('service ' + env.project_name + ' start')


@task
def stop():
    utilities.notify(u'Stopping the app server.')

    sudo('service ' + env.project_name + ' stop')


@task
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service ' + env.project_name + ' restart')
