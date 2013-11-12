from fabric.api import env, task, sudo, run, prefix
from . import utilities


@task
def initial_data(data_files=env.initial_data):
    utilities.notify(u'Loading initial data.')

    with prefix(env.workon):
        for f in data_files:
            run('python manage.py loaddata ' + f)
        run(env.deactivate)


@task
def create(user=env.db_user, name=env.db_name):
    utilities.notify(u'Creating a new database.')

    sudo('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=env.db_name):
    utilities.alert(u'Dropping the database.')

    sudo('dropdb {name}'.format(name=name))


@task
def rebuild(user=env.db_user, name=env.db_name):
    utilities.warn(u'Rebuilding the database.')

    drop(name)
    create(user, name)


@task
def createuser(name=env.db_user):
    utilities.notify(u'Creating a new database user.')

    sudo('createuser --createdb {name}'.format(name=name))


@task
def load(source=env.db_dump_file):
    utilities.notify(u'Loading data into the database.')

    rebuild()
    run('psql ' + env.db_name + ' < ' + source)


@task
def dump(destination=env.db_dump_file):
    utilities.notify(u'Creating a dump of the current database.')

    run('pg_dump ' + env.db_name + ' > ' + destination)
