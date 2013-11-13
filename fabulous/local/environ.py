from fabric.api import env, task, local, prefix
from fabulous import utilities


@task
def ensure(extended='no'):
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip(extended=extended)


@task
def pip(extended='no'):
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    local('pip install -U -r requirements.txt')
