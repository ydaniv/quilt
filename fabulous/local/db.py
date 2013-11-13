from fabric.api import env, task, local, prefix
from fabulous import utilities


@task
def initial_data(data_files=env.initial_data):
    utilities.notify(u'Loading initial data.')

    for f in data_files:
        local('python manage.py loaddata ' + f)


@task
def create(user=env.db_user, name=env.db_name):
    utilities.notify(u'Creating a new database.')

    local('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=env.db_name):
    utilities.alert(u'Dropping the database.')

    local('dropdb {name}'.format(name=name))


@task
def rebuild(user=env.db_user, name=env.db_name):
    utilities.warn(u'Rebuilding the database.')

    drop(name)
    create(user, name)


@task
def createuser(name=env.db_user):
    utilities.notify(u'Creating a new database user.')

    local('createuser --createdb {name}'.format(name=name))


@task
def load(source=env.db_dump_file):
    utilities.notify(u'Loading data into the database.')

    rebuild()
    local('psql ' + env.db_name + ' < ' + source)


@task
def dump(destination=env.db_dump_file):
    utilities.notify(u'Creating a dump of the current database.')

    local('pg_dump ' + env.db_name + ' > ' + destination)
