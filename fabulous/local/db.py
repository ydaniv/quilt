from fabric.api import env, task, local, prefix
from fabulous import utilities


@task
def initial_data():
    utilities.notify(u'Loading initial data.')

    for f in env.initial_data:
        local('python manage.py loaddata ' + f)


@task
def create():
    utilities.notify(u'Creating a new database.')

    local('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=env.db_user, name=env.db_name))


@task
def drop():
    utilities.alert(u'Dropping the database.')

    local('dropdb {name}'.format(name=env.db_name))


@task
def rebuild():
    utilities.warn(u'Rebuilding the database.')

    drop()
    create()


@task
def createuser():
    utilities.notify(u'Creating a new database user.')

    local('createuser --createdb {name}'.format(name=env.db_user))


@task
def load():
    utilities.notify(u'Loading data into the database.')

    rebuild()
    local('psql ' + env.db_name + ' < ' + env.db_dump_file)


@task
def dump():
    utilities.notify(u'Creating a dump of the current database.')

    local('pg_dump ' + env.db_name + ' > ' + env.db_dump_file)
