from fabric.api import env, task, local
from quilt import utilities
from . import environ, machine, proxy, app, db, queue, cache


@task
def bootstrap(initial='no', environment='no', clear_cache='no'):
    utilities.notify(u'Bootstrapping the project. Hold on tight.')

    if initial == 'yes':
        db.create()
    else:
        db.rebuild()

    migrate()
    db.initial_data()

    if environment == 'yes':
        env.ensure()

    if clear_cache == 'yes':
        cache.flush()


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
    local('git checkout ' + env.repository_branch)


@task
def fetch():
    utilities.notify(u'Now fetching from the remote repository.')

    local('git fetch')


@task
def merge():
    utilities.notify(u'Now merging from the remote repository.')

    local('git merge ' + env.repository_branch + ' origin/' + env.repository_branch)
    local('git checkout ' + env.repository_branch)


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
def clean_up():
    utilities.notify(u'Doing a cleanup.')

    utilities.clean_pyc(env.project_root + '/' + env.project_name)


@task
def test():
    utilities.notify(u'Running the project test suite.')

    project_namespace = env.project_name + '.apps.'
    project_apps = []

    for a in env.project_packages:
       if a.startswith(project_namespace):
           project_apps.append(a[len(project_namespace):])

    local('python manage.py test ' + ' '.join(project_apps))


@task
def sanity():
    utilities.notify(u'Starting the project sanity check. Here come the notifications:\n')

    utilities.sanity_check()


@task
def command(cmd):
    utilities.notify(u'Now executing the command you passed.')

    local(cmd)
