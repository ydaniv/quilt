from fabric.api import env, task, local
import cuisine
from quilt import utilities


@task
def ensure():
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip()


@task
def ensure_settings():
    utilities.notify(u'Configuring local settings.')

    context = env
    content = cuisine.text_template(env.project_config_template, context)
    cuisine.file_write(env.project_config_file, content)


@task
def pip():
    utilities.notify(u'Ensuring all Python dependencies are present.')

    local('pip install -U -r requirements.txt')


@task
def bower():
    utilities.notify(u'Ensuring all client-side dependencies are present.')

    local('bower install')


@task
def npm():
    utilities.notify(u'Ensuring all Node.js dependencies are present.')

    local('npm install')
