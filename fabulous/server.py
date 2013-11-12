import cuisine
from fabric.api import env, task, roles, sudo
from fabulous import templates
from fabulous import utilities


@task
@roles('web')
def start():
    utilities.notify(u'Starting the app server.')
    sudo('service ' + env.project_name + ' start')


@task
@roles('web')
def stop():
    utilities.notify(u'Stopping the app server.')
    sudo('service ' + env.project_name + ' stop')


@task
@roles('web')
def restart():
    utilities.notify(u'Restarting the app server.')

    sudo('service ' + env.project_name + ' restart')


@task
@roles('web')
def nginx():
    utilities.notify(u'Configuring nginx.')

    context = env
    context.update({'domain_names': ' '.join(env.allowed_hosts)})
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + env.project_name, content)
    sudo('service nginx restart')


@task
@roles('web')
def gunicorn():
    utilities.notify(u'Configuring gunicorn.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn, context)
    cuisine.file_write('/etc/init/' + env.project_name + '.conf', content)
    restart()


@task
@roles('web')
def celery():
    utilities.notify(u'Configuring celery.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.celery, context)
    cuisine.file_write('/etc/init/' + env.project_name + 'q.conf', content)
    sudo('service ' + env.project_name + 'q restart')
    restart()
