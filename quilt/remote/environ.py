from fabric.api import env, task, roles, run, prefix, execute
import cuisine
from quilt import utilities


@roles('app')
@task
def make():
    utilities.notify(u'Making the virtual environment.')

    run('mkvirtualenv ' + env.project_name)
    run('mkdir ' + env.project_root)
    run('setvirtualenvproject ' + env.project_env + ' ' + env.project_root)


@roles('app')
@task
def destroy():
    utilities.notify(u'Destroying the whole virtual environment.')

    run('rmvirtualenv ' + env.project_name)
    run('rm -r ' + env.project_root)


@roles('app')
@task
def clean():
    utilities.notify(u'Clean all dependencies in the virtual environment.')

    run('rmvirtualenv ' + env.project_name)
    run('mkvirtualenv ' + env.project_name)
    run('setvirtualenvproject ' + env.project_env + ' ' + env.project_root)


@task
def ensure():
    utilities.notify(u'Ensuring all project dependencies are present.')

    execute(pip)
    execute(ensure_settings)


@roles('app')
@task
def ensure_settings():
    utilities.notify(u'Configuring production settings.')

    with prefix(env.workon):
        context = env
        content = cuisine.text_template(env.target_settings_data, context)
        cuisine.file_write(env.target_settings_destination, content)
        run(env.deactivate)


@roles('app')
@task
def pip():
    utilities.notify(u'Ensuring all pip-managed Python dependencies are present.')

    with prefix(env.workon):
        run('pip install -U -r requirements.txt')
        run(env.deactivate)
