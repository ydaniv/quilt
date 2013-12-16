from fabric.api import env, task, local
from fabulous import utilities


@task
def start():
    utilities.notify(u'Starting the q server.')

    local('python manage.py rqworker default')
