import logging
from fabric.api import task, roles, run, prefix
import cuisine
from fabulous import templates
from fabulous.utilities import notify
from fabulous.config import CONFIG, WORKON, DEACTIVATE

try:
    from fabfile.sensitive import SENSITIVE

except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
def make():
    run('mkvirtualenv ' + CONFIG['project_name'])
    run('mkdir ' + CONFIG['project_root'])
    run('setvirtualenvproject ' + CONFIG['project_env'] + ' ' + CONFIG['project_root'])


@task
def settings():
    notify(u'Configuring production settings.')
    with prefix(WORKON):
        context = CONFIG
        context.update(SENSITIVE)
        content = cuisine.text_template(templates.production_settings, context)
        cuisine.file_write(CONFIG['project_root'] + CONFIG['project_name'] +
                           '/settings/production.py', content)
        run(DEACTIVATE)


@task
def ensure(extended='no'):
    notify(u'Ensuring all project dependencies are present.')
    pip(extended=extended)


@task
def pip(extended='no'):
    notify(u'Ensuring all pip-managed Python dependencies are present.')
    with prefix(WORKON):
        run('pip install -U -r requirements/base.txt')
        if extended == 'yes':
            run('pip install -U -r requirements/extended.txt')
        run(DEACTIVATE)
