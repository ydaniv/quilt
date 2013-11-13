from fabric.api import env, task, local
from fabulous import config, utilities

env.update(config.FABULOUS_DEFAULT)

from . import cache, db, environ, server


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
def upgrade():
    utilities.notify(u'Now starting the project upgrade sequence.')

    fetch()
    merge()
    environ.ensure()
    validate()
    migrate()


@task
def clone():
    utilities.notify(u'Now cloning from the remote repository.')

    local('git clone ' + env.repository_location + ' .')


@task
def fetch():
    utilities.notify(u'Now fetching from the remote repository.')

    local('git fetch')


@task
def merge():
    utilities.notify(u'Now merging from the remote repository.')

    local('git merge ' + env.repository_work_branch + ' origin/' + env.repository_work_branch)


@task
def validate():
    utilities.notify(u'Now running Django validations.')

    local('python manage.py validate')


@task
def migrate():
    utilities.notify(u'Now running Django migrations.')

    local('python manage.py syncdb --noinput --migrate')


@task
def collectstatic():
    utilities.notify(u'Now running Django static asset collector.')

    local('python manage.py collectstatic')


@task
def clean_up(root_for_clean=env.project_root):
    utilities.notify(u'Doing a cleanup.')
    utilities.clean_pyc(root_for_clean)


@task
def test():
    utilities.notify(u'Running the project test suite.')

    project_namespace = env.project_name + '.apps.'
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
