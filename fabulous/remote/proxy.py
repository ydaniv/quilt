import cuisine
from fabric.api import env, task, sudo
from fabulous import utilities, contrib


@task
def ensure():
    utilities.notify(u'Configuring nginx.')

    context = env
    context.update({'domain_names': ' '.join(env.project_allowed_hosts)})
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + env.project_name, content)
    restart()


@task
def start():
    utilities.notify(u'Starting the app server.')

    sudo('service nginx start')


@task
def stop():
    utilities.notify(u'Stopping the app server.')

    sudo('service nginx start')


@task
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service nginx start')
