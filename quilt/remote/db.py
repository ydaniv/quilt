from fabric.api import env, task, roles, run, prefix
from quilt import utilities


@roles(utilities.get_role('db'))
@task
def initial_data():
    utilities.notify(u'Loading initial data.')

    with prefix(env.workon):
        for f in env.initial_data:
            run('python manage.py loaddata ' + f)
        run(env.deactivate)


@roles(utilities.get_role('db'))
@task
def create():
    utilities.notify(u'Creating a new database.')

    run('createdb --template template0 --encoding UTF-8 '
        '--owner {user} {name}'.format(user=env.db_user, name=env.db_name))


@roles(utilities.get_role('db'))
@task
def drop():
    utilities.alert(u'Dropping the database.')

    run('dropdb {name}'.format(name=env.db_name))


@roles(utilities.get_role('db'))
@task
def rebuild():
    utilities.warn(u'Rebuilding the database.')

    drop()
    create()


@roles(utilities.get_role('db'))
@task
def drop_connections():
    utilities.warn(u'Drop all active connections.')

    run('psql --pset=format=unaligned -c "SELECT pg_terminate_backend(pg_stat_activity.pid) '
          'FROM pg_stat_activity WHERE pg_stat_activity.datname = ' + '\'' + env.db_name + '\'' +
          ' AND pid <> pg_backend_pid();"')


@roles(utilities.get_role('db'))
@task
def createuser():
    utilities.notify(u'Creating a new database user.')

    run('createuser --createdb {name}'.format(name=env.db_user))


@roles(utilities.get_role('db'))
@task
def load():
    utilities.notify(u'Loading data into the database.')

    rebuild()
    run('psql ' + env.db_name + ' < ' + env.db_dump_file)


@roles(utilities.get_role('db'))
@task
def dump():
    utilities.notify(u'Creating a dump of the current database.')

    run('pg_dump ' + env.db_name + ' > ' + env.db_dump_file)
