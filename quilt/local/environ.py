from fabric.api import task, local
from quilt import utilities


@task
def ensure():
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip()
    bower()
    npm()


@task
def pip():
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    local('pip install -U -r requirements.txt')


@task
def bower():
    utilities.notify(u'Ensuring all bower-managed Javascript dependencies are present.')

    local('bower install')


@task
def npm():
    utilities.notify(u'Ensuring all bower-managed Javascript dependencies are present.')

    local('npm install')
