import logging
from fabric.api import prefix, task, roles, run
from fabulous import config
from fabulous import utilities
from fabulous.remote import db
from fabulous.remote import cache
from fabulous.remote import env
from fabulous.remote import server

try:
    from fabfile.sensitive import SENSITIVE
except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
@roles('web')
def bootstrap():
    utilities.notify(u'Now starting the project bootstrap sequence.')

    env.make()
    clone()
    env.ensure()
    env.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    server.celery()


@task
@roles('web')
def upgrade():
    utilities.notify(u'Now starting the project upgrade sequence.')

    fetch()
    merge()
    env.ensure()
    env.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    server.celery()


@task
@roles('web')
def deploy():
    utilities.notify(u'Now starting the project deploy sequence.')

    fetch()
    merge()
    validate()
    migrate()
    collectstatic()
    server.restart()


@task
@roles('web')
def clone():
    utilities.notify(u'Now cloning from the remote repository.')

    with prefix(config.WORKON):
        run('git clone ' + config.CONFIG['repository_location'] + ' .')
        run(config.DEACTIVATE)


@task
@roles('web')
def fetch():
    utilities.notify(u'Now fetching from the remote repository.')

    with prefix(config.WORKON):
        run('git fetch')
        run(config.DEACTIVATE)


@task
@roles('web')
def merge():
    utilities.notify(u'Now merging from the remote repository.')

    with prefix(config.WORKON):
        run('git merge ' + config.CONFIG['repository_branch'] + ' origin/' + config.CONFIG['repository_branch'])
        run(config.DEACTIVATE)


@task
@roles('web')
def validate():
    utilities.notify(u'Now running Django validations.')

    with prefix(config.WORKON):
        run('python manage.py validate')
        run(config.DEACTIVATE)


@task
@roles('web')
def migrate():
    utilities.notify(u'Now running Django migrations.')

    with prefix(config.WORKON):
        run('python manage.py syncdb --noinput --migrate')
        run(config.DEACTIVATE)


@task
@roles('web')
def collectstatic():
    utilities.notify(u'Now running Django static asset collector.')

    with prefix(config.WORKON):
        run('python manage.py collectstatic')
        run(config.DEACTIVATE)


@task
@roles('web')
def command(cmd):
    utilities.notify(u'Now executing the command you passed.')

    with prefix(config.WORKON):
        run(cmd)
        run(config.DEACTIVATE)
    server.restart()
