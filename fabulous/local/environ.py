from fabric.api import env, task, roles, run, prefix
from fabulous import utilities


@task
def ensure(extended='no'):
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip(extended=extended)


@task
def pip(extended='no'):
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    run('pip install -U -r requirements/base.txt')
    if extended == 'yes':
        run('pip install -U -r requirements/extended.txt')
