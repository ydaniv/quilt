from fabric.api import task, local
from fabulous import utilities
from fabulous import config


@task
def initial_data(fixtures=config.CONFIG['project_initial_data']['local']):
    utilities.notify(u'Loading initial data.')
    for fixture in fixtures:
        local('python manage.py loaddata ' + fixture)


@task
def create(user=config.CONFIG['db_user'], name=config.CONFIG['db_name']):
    utilities.notify(u'Creating a new database.')
    local('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=config.CONFIG['db_name']):
    utilities.alert(u'Dropping the database.')
    local('dropdb {name}'.format(name=name))


@task
def rebuild(user=config.CONFIG['db_user'], name=config.CONFIG['db_name']):
    utilities.warn(u'Rebuilding the database.')
    drop(name)
    create(user, name)


@task
def createuser(name=config.CONFIG['db_user']):
    utilities.notify(u'Creating a new database user.')
    local('createuser --createdb {name}'.format(name=name))


@task
def load(source=config.CONFIG['db_dump_file']):
    utilities.notify(u'Loading data into the database.')
    rebuild()
    local('psql ' + config.CONFIG['db_name'] + ' < ' + source)



@task
def dump(destination=config.CONFIG['db_dump_file']):
    utilities.notify(u'Creating a dump of the current database.')
    local('pg_dump ' + config.CONFIG['db_name'] + ' > ' + destination)
