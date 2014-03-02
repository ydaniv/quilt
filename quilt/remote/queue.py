import cuisine
from fabric.api import env, execute, task, roles, sudo
from quilt import utilities


@roles('queue')
@task
def ensure():
    """Ensures the Queue configuration and process management is in place."""

    utilities.notify(u'Ensuring the queue is configured correctly.')

    execute(config)
    execute(management)


@roles('queue')
@task
def config():
    """Ensures the Queue configuration is in place."""

    utilities.notify(u'Ensuring the queue configuration settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.queue_config_template, context)
    cuisine.file_write(env.queue_config_file, content)
    execute(restart)


@roles('queue')
@task
def management():
    """Ensures the Queue process management is in place."""

    utilities.notify(u'Ensuring the queue management settings.')

    context = env
    cuisine.mode_sudo()
    content = cuisine.text_template(env.queue_management_template, context)
    cuisine.file_write(env.queue_management_file, content)
    execute(restart)


@roles('queue')
@task
def start():
    """Start the Queue process."""

    utilities.notify(u'Starting the queue server.')

    sudo(env.queue_command_start)


@roles('queue')
@task
def stop():
    """Stop the Queue process."""

    utilities.notify(u'Stopping the queue server.')

    sudo(env.queue_command_stop)


@roles('queue')
@task
def restart():
    """Restart the Queue process."""

    utilities.notify(u'Restarting the queue server.')

    sudo(env.queue_command_restart)
