import os
import shutil
from fabric.api import task, local, lcd
from fabfile.utilities import notify
from fabfile.local import db
from fabfile.config import CONFIG


@task
def init():
    notify(u'Loading the project initial data state.')
    local('python manage.py loaddata dev/sites.json')


@task
def clone():
    notify(u'Cloning the data repository.')
    with lcd(CONFIG['dataset_root']):
        local('git clone ' + CONFIG['dataset_repo'] + ' dataset')


@task
def fetch():
    notify(u'Fetching new commits from the data repository.')
    with lcd(CONFIG['dataset_root'] + '/dataset'):
        local('git fetch')


@task
def merge():
    notify(u'Merging latest changes from the data repository.')
    with lcd(CONFIG['dataset_root'] + '/dataset'):
        local('git merge ' + CONFIG['dataset_branch'] + ' origin/' + CONFIG['dataset_branch'])


@task
def pull():
    notify(u'Pulling latest changes from the data repository.')
    fetch()
    merge()


@task
def push():
    notify(u'Pushing latest local changes to the data repository.')
    with lcd(CONFIG['dataset_root'] + '/dataset'):
        local('git push origin/' + CONFIG['dataset_branch'])


@task
def load(from_dump='no', source=CONFIG['db_dump_file']):
    notify(u'Loading data into the database.')

    if from_dump == 'yes':
        notify(u'Loading data from a postgresql dump source.')
        db.drop()
        db.create()
        local('psql ' + CONFIG['db_name'] + ' < ' + source)

    else:
        notify(u'Loading data from a data repository.')

        data_root = CONFIG['dataset_root'] + '/dataset/data'
        pass


@task
def dump(destination=CONFIG['db_dump_file']):
    notify(u'Creating a dump of the current database.')
    local('pg_dump ' + CONFIG['db_name'] + ' > ' + destination)


@task
def sync():
    notify(u'Syncing data to supported services.')
    pass
