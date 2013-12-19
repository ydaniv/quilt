import cuisine
from fabric.api import env, task, roles, sudo
from quilt import utilities, contrib


@roles('proxy')
@task
def ensure():
    utilities.notify(u'Configuring the proxy server.')

    context = env
    context.update({'domain_names': ' '.join(env.project_allowed_hosts)})
    cuisine.mode_sudo()
    content = cuisine.text_template(contrib.templates.proxy, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + env.project_name, content)
    restart()


@roles('proxy')
@task
def start():
    utilities.notify(u'Starting the proxy server.')

    sudo('service nginx start')


@roles('proxy')
@task
def stop():
    utilities.notify(u'Stopping the proxy server.')

    sudo('service nginx start')


@roles('proxy')
@task
def restart():
    utilities.notify(u'Restarting the proxy server.')

    sudo('service nginx start')
