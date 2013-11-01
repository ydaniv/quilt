from fabric.api import task, local
from fabulous.utilities import notify, warn, alert
from fabulous.config import CONFIG


@task
def initial_data(data_files=CONFIG['db_initial_data']['remote']):
    for f in data_files:
        local('python manage.py loaddata ' + f)


@task
def create(user=CONFIG['db_user'], name=CONFIG['db_name']):
    notify(u'Creating a new database.')
    local('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=CONFIG['db_name']):
    alert(u'Dropping the database.')
    local('dropdb {name}'.format(name=name))


@task
def rebuild(user=CONFIG['db_user'], name=CONFIG['db_name']):
    warn(u'Rebuilding the database.')
    drop(name)
    create(user, name)


@task
def createuser(name=CONFIG['db_user']):
    notify(u'Creating a new database user.')
    local('createuser --createdb {name}'.format(name=name))


@task
def load(source=CONFIG['db_dump_file']):
    notify(u'Loading data into the database.')
    rebuild()
    local('psql ' + CONFIG['db_name'] + ' < ' + source)



@task
def dump(destination=CONFIG['db_dump_file']):
    notify(u'Creating a dump of the current database.')
    local('pg_dump ' + CONFIG['db_name'] + ' > ' + destination)
