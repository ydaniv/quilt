import logging
from fabric.api import env, prefix, task, roles, run
from fabulous import cache, db, environ, server, utilities


try:
    from fabfile.sensitive import SENSITIVE
except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


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
