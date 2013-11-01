from fabric.api import task, sudo, run, prefix
from fabulous.utilities import notify, warn, alert
from fabulous.config import CONFIG, WORKON, DEACTIVATE


@task
def initial_data(data_files=CONFIG['db_initial_data']['remote']):
    with prefix(WORKON):
        for f in data_files:
            run('python manage.py loaddata ' + f)
        run(DEACTIVATE)


@task
def create(user=CONFIG['db_user'], name=CONFIG['db_name']):
    notify(u'Creating a new database.')
    sudo('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=CONFIG['db_name']):
    alert(u'Dropping the database.')
    sudo('dropdb {name}'.format(name=name))


@task
def rebuild(user=CONFIG['db_user'], name=CONFIG['db_name']):
    warn(u'Rebuilding the database.')
    drop(name)
    create(user, name)


@task
def createuser(name=CONFIG['db_user']):
    notify(u'Creating a new database user.')
    sudo('createuser --createdb {name}'.format(name=name))


@task
def load(source=CONFIG['db_dump_file']):
    notify(u'Loading data into the database.')
    rebuild()
    run('psql ' + CONFIG['db_name'] + ' < ' + source)


@task
def dump(destination=CONFIG['db_dump_file']):
    notify(u'Creating a dump of the current database.')
    run('pg_dump ' + CONFIG['db_name'] + ' > ' + destination)
