import logging
import importlib
from fabric.api import env, prefix, task, roles, run
from . import config

env.update(config.FABULOUS_DEFAULT)

from . import cache, db, environ, server, utilities


@task
def e(environment=None):
    utilities.notify(u'Setting the environment for this task run.')

    # if no environment name passed, we work on local
    activated_environment = u'LOCAL'
    env.roles = 'local'

    if environment:
        project_config = importlib.import_module('fabfile.config')
        project_sensitive = importlib.import_module('fabfile.sensitive')
        env_config = getattr(project_config, environment.upper())
        env_sensitive = getattr(project_sensitive, environment.upper() + '_SENSITIVE')
        env.update(env_config)
        env.update(env_sensitive)

        env.roles = [environment]

        activated_environment = unicode(environment.upper())

    utilities.notify(u'The execution environment is ' + activated_environment)


@task
def build_remote():
    utilities.notify(u'Now starting the project bootstrap sequence.')

    environ.make()
    clone()
    environ.ensure()
    environ.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    server.celery()


@task
def upgrade():
    utilities.notify(u'Now starting the project upgrade sequence.')

    fetch()
    merge()
    environ.ensure()
    environ.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    server.celery()


@task
def deploy():
    utilities.notify(u'Now starting the project deploy sequence.')

    fetch()
    merge()
    validate()
    migrate()
    collectstatic()
    server.restart()


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
def clone():
    utilities.notify(u'Now cloning from the remote repository.')

    with prefix(env.workon):
        run('git clone ' + env.repository_location + ' .')
        run(env.deactivate)


@task
def fetch():
    utilities.notify(u'Now fetching from the remote repository.')

    with prefix(env.workon):
        run('git fetch')
        run(env.deactivate)


@task
def merge():
    utilities.notify(u'Now merging from the remote repository.')

    with prefix(env.workon):
        run('git merge ' + env.repository_work_branch + ' origin/' + env.repository_work_branch)
        run(env.deactivate)


@task
def validate():
    utilities.notify(u'Now running Django validations.')

    with prefix(env.workon):
        run('python manage.py validate')
        run(env.deactivate)


@task
def migrate():
    utilities.notify(u'Now running Django migrations.')

    with prefix(env.workon):
        run('python manage.py syncdb --noinput --migrate')
        run(env.deactivate)


@task
def collectstatic():
    utilities.notify(u'Now running Django static asset collector.')

    with prefix(env.workon):
        run('python manage.py collectstatic')
        run(env.deactivate)


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

    with prefix(env.workon):
        run(cmd)
        run(env.deactivate)
