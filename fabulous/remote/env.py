import logging
from fabric.api import task, roles, run, prefix
import cuisine
from fabulous import templates
from fabulous import utilities
from fabulous import config

try:
    from fabfile.sensitive import SENSITIVE

except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
def make():
    utilities.notify(u'Making the virtual environment.')

    run('mkvirtualenv ' + config.CONFIG['project_name'])
    run('mkdir ' + config.CONFIG['project_root'])
    run('setvirtualenvproject ' + config.CONFIG['project_env'] + ' ' + config.CONFIG['project_root'])


@task
def settings():
    utilities.notify(u'Configuring production settings.')

    with prefix(config.WORKON):
        context = config.CONFIG
        context.update(SENSITIVE)
        content = cuisine.text_template(templates.production_settings, context)
        cuisine.file_write(config.CONFIG['project_root'] + config.CONFIG['project_name'] +
                           '/settings/production.py', content)
        run(config.DEACTIVATE)


@task
def ensure(extended='no'):
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip(extended=extended)


@task
def pip(extended='no'):
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    with prefix(config.WORKON):
        run('pip install -U -r requirements/base.txt')
        if extended == 'yes':
            run('pip install -U -r requirements/extended.txt')
        run(config.DEACTIVATE)
