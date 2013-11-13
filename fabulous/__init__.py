import importlib
from fabric.api import env, task
from fabulous import config, utilities

env.update(config.FABULOUS_DEFAULT)

from fabulous.local import *
from fabulous import remote


@task
def e(environment=None):
    utilities.notify(u'Setting the environment for this task run.')

    # if no environment name passed, we work on local
    activated_environment = u'LOCAL'

    if environment:
        # TODO: We let this fail if anything here is not found. Handle in a more friendly fashion.
        project_config = importlib.import_module('fabfile.config')
        project_sensitive = importlib.import_module('fabfile.sensitive')
        env_config = getattr(project_config, environment.upper())
        env_sensitive = getattr(project_sensitive, environment.upper() + '_SENSITIVE')
        env.update(env_config)
        env.update(env_sensitive)

        env.roles = [environment]

        activated_environment = unicode(environment.upper())

    utilities.notify(u'The execution environment is ' + activated_environment)