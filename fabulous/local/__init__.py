from fabric.api import task, local
from fabulous.config import CONFIG
from fabulous.local import db
from fabulous.local import cache
from fabulous.local import env
from fabulous.utilities import notify, sanity_check


@task
def bootstrap(initial='no', environment='no', clear_cache='no'):
    notify(u'Bootstrapping the project. Hold on tight.')

    if initial == 'yes':
        db.create()
    else:
        db.rebuild()

    if environment == 'yes':
        env.ensure()

    if clear_cache == 'yes':
        cache.flush()

    migrate()


@task
def migrate():
    notify(u'Running Django syncdb and migrations.')
    local('python manage.py syncdb --noinput --migrate')


@task
def test():
    notify(u'Running the project test suite.')
    project_namespace = CONFIG['project_name'] + '.apps.'
    project_apps = []

    for app in settings.INSTALLED_APPS:
        if app.startswith(project_namespace):
            project_apps.append(app[len(project_namespace):])

    local('python manage.py test ' + ' '.join(project_apps))


@task
def sanity():
    notify(u'Starting the project sanity check. Here come the notifications:\n')
    sanity_check()


@task
def command(command):
    notify(u'Running what you passed as a command.')
    local(command)
