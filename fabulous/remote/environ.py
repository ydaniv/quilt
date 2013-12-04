from fabric.api import env, task, run, prefix
import cuisine
from fabulous import utilities


@task
def make():
    utilities.notify(u'Making the virtual environment.')

    run('mkvirtualenv ' + env.project_name)
    run('mkdir ' + env.project_root)
    run('setvirtualenvproject ' + env.project_env + ' ' + env.project_root)


@task
def ensure():
    utilities.notify(u'Ensuring all project dependencies are present.')

    pip()
    ensure_settings()


@task
def ensure_settings():
    utilities.notify(u'Configuring production settings.')

    with prefix(env.workon):
        context = env
        content = cuisine.text_template(env.target_settings_data, context)
        cuisine.file_write(env.target_settings_destination, content)
        run(env.deactivate)


@task
def pip():
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    with prefix(env.workon):
        run('pip install -U -r requirements.txt')
        run(env.deactivate)
