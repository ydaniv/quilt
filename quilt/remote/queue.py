import cuisine
from fabric.api import env, task, roles, sudo
from quilt import utilities, contrib


@roles('queue')
@task
def ensure():
    utilities.notify(u'Configuring the queue.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.queue, context)
    cuisine.file_write('/etc/init/' + env.project_name + 'q.conf', content)
    restart()


@roles('queue')
@task
def start():
    utilities.notify(u'Starting the queue server.')

    sudo('service ' + env.project_name + 'q start')


@roles('queue')
@task
def stop():
    utilities.notify(u'Stopping the queue server.')

    sudo('service ' + env.project_name + 'q stop')


@roles('queue')
@task
def restart():
    utilities.notify(u'Restarting the queue server.')

    sudo('service ' + env.project_name + 'q restart')
