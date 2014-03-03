from fabric.api import env, task, local
from quilt import utilities
from . import environ, machine, proxy, app, db, queue, cache, vcs


@task
def bootstrap(initial='no', environment='no', clear_cache='no'):
    """A sequence the cleans and rebuilds the project environment."""

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
    """A sequence that upgrades the project codebase and dependencies."""

    utilities.notify(u'Now starting the project upgrade sequence.')

    vcs.fetch()
    vcs.merge()
    environ.ensure()
    validate()
    migrate()


@task
def validate():
    """Run validation checks over the codebase."""

    utilities.notify(u'Now running Django validations.')

    local('python manage.py validate')


@task
def migrate():
    """Run data migrations for the project."""

    utilities.notify(u'Now running Django migrations.')

    local('python manage.py syncdb --noinput --migrate')


@task
def collectstatic():
    """Run static resource management for the project."""

    utilities.notify(u'Now running Django static asset collector.')

    local('python manage.py collectstatic')


@task
def clean_up():
    """Clean the project of all .pyc files."""

    utilities.notify(u'Doing a cleanup.')

    utilities.clean_pyc(env.project_root + '/' + env.project_name)


@task
def test():
    """Run tests for the project code."""

    utilities.notify(u'Running the project test suite.')

    project_namespace = env.project_name + '.apps.'
    project_apps = []

    for a in env.project_packages:
        if a.startswith(project_namespace):
            project_apps.append(a[len(project_namespace):])

    local('python manage.py test ' + ' '.join(project_apps))


@task
def sanity():
    """Run a check on all project dependencies."""

    utilities.notify(u'Starting the project sanity check. '
                     'Here come the notifications:\n')

    utilities.sanity_check()


@task
def command(cmd):
    """Execute a command."""

    utilities.notify(u'Now executing the command you passed.')

    local(cmd)
