import cuisine
from fabric.api import task, roles, sudo
from fabfile import templates
from fabfile.utilities import notify
from fabfile.config import CONFIG


@task
@roles('web')
def start():
    sudo('service _____ start')


@task
@roles('web')
def stop():
    sudo('service _____ stop')


@task
@roles('web')
def restart():
    sudo('service _____ restart')


@task
@roles('web')
def nginx():
    notify('Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('________', content)
    sudo('service nginx restart')


@task
@roles('web')
def gunicorn():
    notify('Configuring gunicorn.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn, context)
    cuisine.file_write('/etc/init/gunicorn.conf', content)
    restart()
