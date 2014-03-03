from fabric.api import env, prefix, task, roles, run, execute
from quilt import utilities
from . import environ, machine, proxy, app, db, queue, cache, vcs


@task
def build():
    """A sequence that makes the initial build of the project environment."""

    utilities.notify(u'Now building out the remote environment.')

    execute(environ.make)
    execute(vcs.clone)
    execute(environ.ensure)
    execute(db.create)
    execute(validate)
    execute(migrate)
    execute(db.initial_data)
    execute(collectstatic)
    execute(proxy.ensure)
    execute(app.ensure)
    execute(queue.ensure)


@task
def bootstrap(initial='no', environment='no', clear_cache='no'):
    """A sequence the cleans and rebuilds the project environment."""

    utilities.notify(u'Bootstrapping the project. Hold on tight.')

    if initial == 'yes':
        execute(db.create)
    else:
        execute(db.rebuild)

    execute(migrate)
    execute(db.initial_data)

    if environment == 'yes':
        execute(env.ensure)

    if clear_cache == 'yes':
        execute(cache.flush)

    execute(app.restart)
    execute(proxy.restart)


@task
def upgrade():
    """A sequence that upgrades the project codebase and dependencies."""

    utilities.notify(u'Now starting the project upgrade sequence.')

    execute(vcs.fetch)
    execute(vcs.merge)
    execute(environ.ensure)
    execute(validate)
    execute(migrate)
    execute(collectstatic)
    execute(proxy.ensure)
    execute(app.ensure)
    execute(queue.ensure)


@task
def deploy():
    """A sequence that deploys new code to a target."""

    utilities.notify(u'Now starting the project deploy sequence.')

    execute(vcs.fetch)
    execute(vcs.merge)
    execute(validate)
    execute(migrate)
    execute(collectstatic)
    execute(app.restart)
    execute(proxy.restart)


@roles('app')
@task
def validate():
    """Run validation checks over the codebase."""

    utilities.notify(u'Now running Django validations.')

    with prefix(env.workon):
        run('python manage.py validate')
        run(env.deactivate)


@roles('app')
@task
def migrate():
    """Run data migrations for the project."""

    utilities.notify(u'Now running Django migrations.')

    with prefix(env.workon):
        run('python manage.py syncdb --noinput --migrate')
        run(env.deactivate)


@roles('app')
@task
def collectstatic():
    """Run static resource management for the project."""

    utilities.notify(u'Now running Django static asset collector.')

    with prefix(env.workon):
        run('python manage.py collectstatic')
        run(env.deactivate)


@roles('app')
@task
def test():
    """Run tests for the project code."""

    utilities.notify(u'Running the project test suite.')

    project_namespace = env.project_name + '.apps.'
    project_apps = []

    for a in env.project_packages:
        if a.startswith(project_namespace):
            project_apps.append(a[len(project_namespace):])

    run('python manage.py test ' + ' '.join(project_apps))


@roles('app')
@task
def sanity():
    """Run a check on all project dependencies."""

    utilities.notify(u'Starting the project sanity check. '
                     'Here come the notifications:\n')

    utilities.sanity_check()


@roles('app')
@task
def command(cmd, activate='no'):
    """Execute a command."""

    utilities.notify(u'Now executing the command you passed.')

    if activate == 'yes':

        with prefix(env.workon):
            run(cmd)
            run(env.deactivate)
    else:
        run(cmd)
