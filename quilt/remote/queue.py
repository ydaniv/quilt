import cuisine
from fabric.api import env, execute, task, roles, sudo
from quilt import utilities


@roles('queue')
@task
def ensure():
    """Ensures the queue configuration and process management is in place."""

    utilities.notify(u'Ensuring the queue is configured correctly.')

    execute(config)
    execute(management)


@roles('queue')
@task
def config():
    """Ensures the queue configuration is in place."""

    utilities.notify(u'Ensuring the queue configuration settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.queue_config_template, context)
    cuisine.file_write(env.queue_config_file, content)
    execute(restart)


@roles('queue')
@task
def management():
    """Ensures the queue process management is in place."""

    utilities.notify(u'Ensuring the queue management settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.queue_management_template, context)
    cuisine.file_write(env.queue_management_file, content)
    execute(update)
    execute(restart)


@roles('queue')
@task
def start():
    """Start the queue process."""

    utilities.notify(u'Starting the queue server.')

    sudo(env.queue_command_start)


@roles('queue')
@task
def stop():
    """Stop the queue process."""

    utilities.notify(u'Stopping the queue server.')

    sudo(env.queue_command_stop)


@roles('queue')
@task
def restart():
    """Restart the queue process."""

    utilities.notify(u'Restarting the queue server.')

    sudo(env.queue_command_restart)


@roles('queue')
@task
def update():
    """Update the process manager with changes to the queue configration."""

    utilities.notify(u'Updating the queue process manager.')

    sudo(env.queue_command_update)
