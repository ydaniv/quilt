import logging
from fabric.api import env, task, roles, run, prefix
import cuisine
from . import templates, utilities


try:
    from fabfile.sensitive import SENSITIVE

except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
def make():
    utilities.notify(u'Making the virtual environment.')

    run('mkvirtualenv ' + env.project_name)
    run('mkdir ' + env.project_root)
    run('setvirtualenvproject ' + env.project_env + ' ' + env.project_root)


@task
def settings():
    utilities.notify(u'Configuring production settings.')

    with prefix(env.workon):
        context = env
        context.update(SENSITIVE)
        content = cuisine.text_template(templates.production_settings, context)
        cuisine.file_write(env.project_root + env.project_name +
                           '/settings/production.py', content)
        run(env.deactivate)


@task
def ensure(extended='no'):
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip(extended=extended)


@task
def pip(extended='no'):
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    with prefix(env.workon):
        run('pip install -U -r requirements/base.txt')
        if extended == 'yes':
            run('pip install -U -r requirements/extended.txt')
        run(env.deactivate)
