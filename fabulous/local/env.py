from fabric.api import task, local
from fabulous.utilities import notify


@task
def ensure(extended='no'):
    notify(u'Ensuring all project dependencies are present.')
    pip(extended=extended)


@task
def pip(extended='no'):
    notify(u'Ensuring all pip-managed Python dependencies are present.')
    local('pip install -U -r requirements/base.txt')
    if extended == 'yes':
        local('pip install -U -r requirements/extended.txt')