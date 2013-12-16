import cuisine
from fabric.api import env, task, sudo
from fabulous import utilities, contrib


@task
def ensure():
    utilities.notify(u'Configuring rq.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.queue, context)
    cuisine.file_write('/etc/init/' + env.project_name + 'q.conf', content)
    restart()


@task
def start():
    utilities.notify(u'Starting the app server.')

    sudo('service ' + env.project_name + 'q start')


@task
def stop():
    utilities.notify(u'Stopping the app server.')

    sudo('service ' + env.project_name + 'q stop')


@task
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service ' + env.project_name + 'q restart')
