from fabric.api import task, local
from fabulous import config
from fabulous import utilities
from fabulous.local import db
from fabulous.local import cache
from fabulous.local import env


@task
def bootstrap(initial='no', environment='no', clear_cache='no'):
    utilities.notify(u'Bootstrapping the project. Hold on tight.')

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
    utilities.notify(u'Running Django syncdb and migrations.')
    local('python manage.py syncdb --noinput --migrate')


@task
def test():
    utilities.notify(u'Running the project test suite.')

    project_namespace = config.CONFIG['project_name'] + '.apps.'
    project_apps = []

    #for app in django_settings.INSTALLED_APPS:
    #    if app.startswith(project_namespace):
    #        project_apps.append(app[len(project_namespace):])

    #local('python manage.py test ' + ' '.join(project_apps))


@task
def sanity():
    utilities.notify(u'Starting the project sanity check. Here come the notifications:\n')

    utilities.sanity_check()


@task
def command(cmd):
    utilities.notify(u'Now executing the command you passed.')

    local(cmd)
