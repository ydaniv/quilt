import cuisine
from fabric.api import task, roles, sudo
from fabulous import templates
from fabulous.utilities import notify
from fabulous.config import CONFIG


@task
@roles('web')
def start():
    notify(u'Starting the app server.')
    sudo('service ' + CONFIG['project_name'] + ' start')


@task
@roles('web')
def stop():
    notify(u'Stopping the app server.')
    sudo('service ' + CONFIG['project_name'] + ' stop')


@task
@roles('web')
def restart():
    notify(u'Restarting the app server.')
    sudo('service ' + CONFIG['project_name'] + ' restart')


@task
@roles('web')
def nginx():
    notify(u'Configuring nginx.')
    context = CONFIG
    context.update({'domain_names': ' '.join(CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + CONFIG['project_name'], content)
    sudo('service nginx restart')


@task
@roles('web')
def gunicorn():
    notify(u'Configuring gunicorn.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn, context)
    cuisine.file_write('/etc/init/' + CONFIG['project_name'] + '.conf', content)
    restart()


@task
@roles('web')
def celery():
    notify(u'Configuring celery.')
    context = CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.celery, context)
    cuisine.file_write('/etc/init/' + CONFIG['project_name'] + 'q.conf', content)
    sudo('service ' + CONFIG['project_name'] + 'q restart')
    restart()
