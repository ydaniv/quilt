import cuisine
from fabric.api import env, task, execute, roles, sudo
from quilt import utilities


@roles('app')
@task
def ensure():
    """Ensures the app configuration and process management is in place."""

    utilities.notify(u'Ensuring the app is configured correctly.')

    execute(config)
    execute(management)


@roles('app')
@task
def config():
    """Ensures the app configuration is in place."""

    utilities.notify(u'Ensuring the app configuration settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.app_config_template, context)
    cuisine.file_write(env.app_config_file, content)
    execute(restart)


@roles('app')
@task
def management():
    """Ensures the app process management is in place."""

    utilities.notify(u'Ensuring the app management settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.app_management_template, context)
    cuisine.file_write(env.app_management_file, content)
    execute(update)
    execute(restart)


@roles('app')
@task
def start():
    """Start the app process."""

    utilities.notify(u'Starting the app server.')

    sudo(env.app_command_start)


@roles('app')
@task
def stop():
    """Stop the app process."""

    utilities.notify(u'Stopping the app server.')

    sudo(env.app_command_stop)


@roles('app')
@task
def restart():
    """Restart the app process."""

    utilities.notify(u'Restarting the app server.')

    sudo(env.app_command_restart)


@roles('app')
@task
def update():
    """Update the process manager with changes to the app configration."""

    utilities.notify(u'Updating the app process manager.')

    sudo(env.app_command_update)
