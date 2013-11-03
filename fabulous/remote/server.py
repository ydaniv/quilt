import cuisine
from fabric.api import task, roles, sudo
from fabulous import templates
from fabulous import utilities
from fabulous import config


@task
@roles('web')
def start():
    utilities.notify(u'Starting the app server.')
    sudo('service ' + config.CONFIG['project_name'] + ' start')


@task
@roles('web')
def stop():
    utilities.notify(u'Stopping the app server.')
    sudo('service ' + config.CONFIG['project_name'] + ' stop')


@task
@roles('web')
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service ' + config.CONFIG['project_name'] + ' restart')


@task
@roles('web')
def nginx():
    utilities.notify(u'Configuring nginx.')

    context = config.CONFIG
    context.update({'domain_names': ' '.join(config.CONFIG['allowed_hosts'])})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + config.CONFIG['project_name'], content)
    sudo('service nginx restart')


@task
@roles('web')
def gunicorn():
    utilities.notify(u'Configuring gunicorn.')

    context = config.CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn, context)
    cuisine.file_write('/etc/init/' + config.CONFIG['project_name'] + '.conf', content)
    restart()


@task
@roles('web')
def celery():
    utilities.notify(u'Configuring celery.')

    context = config.CONFIG
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.celery, context)
    cuisine.file_write('/etc/init/' + config.CONFIG['project_name'] + 'q.conf', content)
    sudo('service ' + config.CONFIG['project_name'] + 'q restart')
    restart()
