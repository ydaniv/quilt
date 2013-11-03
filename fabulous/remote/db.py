from fabric.api import task, sudo, run, prefix
from fabulous import utilities
from fabulous import config


@task
def initial_data(data_files=config.CONFIG['project_initial_data']['remote']):
    utilities.notify(u'Loading initial data.')

    with prefix(config.WORKON):
        for f in data_files:
            run('python manage.py loaddata ' + f)
        run(config.DEACTIVATE)


@task
def create(user=config.CONFIG['db_user'], name=config.CONFIG['db_name']):
    utilities.notify(u'Creating a new database.')

    sudo('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop(name=config.CONFIG['db_name']):
    utilities.alert(u'Dropping the database.')

    sudo('dropdb {name}'.format(name=name))


@task
def rebuild(user=config.CONFIG['db_user'], name=config.CONFIG['db_name']):
    utilities.warn(u'Rebuilding the database.')

    drop(name)
    create(user, name)


@task
def createuser(name=config.CONFIG['db_user']):
    utilities.notify(u'Creating a new database user.')

    sudo('createuser --createdb {name}'.format(name=name))


@task
def load(source=config.CONFIG['db_dump_file']):
    utilities.notify(u'Loading data into the database.')

    rebuild()
    run('psql ' + config.CONFIG['db_name'] + ' < ' + source)


@task
def dump(destination=config.CONFIG['db_dump_file']):
    utilities.notify(u'Creating a dump of the current database.')

    run('pg_dump ' + config.CONFIG['db_name'] + ' > ' + destination)
