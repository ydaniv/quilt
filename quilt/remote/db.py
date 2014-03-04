from fabric.api import env, task, execute, roles, run, prefix
from fabric import operations
from quilt import utilities


@roles('app')
@task
def initial_data():
    """Load any initial data into the DB."""

    utilities.notify(u'Loading initial data.')

    with prefix(env.workon):
        for f in env.project_initial_data:
            run('python manage.py loaddata ' + f)
        run(env.deactivate)


@roles('db')
@task
def create():
    """Create the DB."""

    utilities.notify(u'Creating a new database.')

    run('createdb --template template0 --encoding UTF-8 '
        '--owner {user} {name}'.format(user=env.db_user, name=env.db_name))


@roles('db')
@task
def drop():
    """Drop the DB."""

    utilities.alert(u'Dropping the database.')

    run('dropdb {name}'.format(name=env.db_name))


@roles('db')
@task
def rebuild():
    """Drop and create the DB again."""

    utilities.warn(u'Rebuilding the database.')

    execute(drop)
    execute(create)


@roles('db')
@task
def terminate_connections():
    """Terminates all active connections to the database."""

    utilities.warn(u'Terminate all active connections.')

    run('psql --pset=format=unaligned -c '
        '"SELECT pg_terminate_backend(pg_stat_activity.pid) '
        'FROM pg_stat_activity WHERE pg_stat_activity.datname = ' +
        '\'' + env.db_name + '\'' + ' AND pid <> pg_backend_pid();"')


@roles('db')
@task
def createuser():
    """Create a DB user."""

    utilities.notify(u'Creating a new database user.')

    run('createuser --createdb {name}'.format(name=env.db_user))


@roles('db')
@task
def load():
    """Load the DB from a valid SQL file."""

    utilities.notify(u'Loading data into the database.')

    execute(rebuild)
    run('psql ' + env.db_name + ' < ' + env.db_dump_file)


@roles('db')
@task
def dump():
    """Dump the DB to file."""

    utilities.notify(u'Creating a dump of the current database.')

    run('pg_dump ' + env.db_name + ' > ' + env.db_dump_file)


@roles('db')
@task
def put(local_file):
    """Put a DB dump, available locally, in the remote dump location."""

    utilities.notify(u'Loading a local db dump to the remote dump location.')

    execute(rebuild)
    operations.put(local_file, env.db_dump_file)
