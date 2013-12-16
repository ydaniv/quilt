from fabric.api import env, prefix, task, run
from quilt import utilities
from . import environ, machine, proxy, app, db, queue, cache


@task
def build():
    utilities.notify(u'Now building out the remote environment.')

    environ.make()
    clone()
    environ.ensure()
    environ.settings()
    validate()
    migrate()
    collectstatic()
    proxy.ensure()
    app.ensure()
    queue.ensure()


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
    proxy.ensure()
    app.ensure()
    queue.ensure()


@task
def deploy():
    utilities.notify(u'Now starting the project deploy sequence.')

    fetch()
    merge()
    validate()
    migrate()
    collectstatic()
    app.restart()
    proxy.restart()


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

    app.restart()
    proxy.restart()


@task
def clone():
    utilities.notify(u'Now cloning from the remote repository.')

    with prefix(env.workon):
        run('git clone ' + env.repository_location + ' .')
        run('git checkout ' + env.repository_deploy_branch)
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
        run('git merge ' + env.repository_deploy_branch + ' origin/' + env.repository_deploy_branch)
        run('git checkout ' + env.repository_deploy_branch)
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
    declared_apps = env.django_settings.INSTALLED_APPS

    for a in declared_apps:
       if a.startswith(project_namespace):
           project_apps.append(a[len(project_namespace):])

    run('python manage.py test ' + ' '.join(project_apps))


@task
def sanity():
    utilities.notify(u'Starting the project sanity check. Here come the notifications:\n')

    utilities.sanity_check()


@task
def command(cmd, activate='no'):
    utilities.notify(u'Now executing the command you passed.')

    if activate == 'yes':

        with prefix(env.workon):
            run(cmd)
            run(env.deactivate)
    else:
        run(cmd)
