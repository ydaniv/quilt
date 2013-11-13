import importlib
from fabric.api import env, task
from fabulous import config, utilities

env.update(config.FABULOUS_DEFAULT)

from fabulous.local import *
from fabulous import remote


@task
def e(environment='local'):
    utilities.notify(u'Setting the environment for this task run.')

    project_config = importlib.import_module('fabfile.config')
    project_sensitive = importlib.import_module('fabfile.sensitive')
    env_config = getattr(project_config, environment.upper())
    env_sensitive = getattr(project_sensitive, environment.upper() + '_SENSITIVE')
    env.update(env_config)
    env.update(env_sensitive)
    env.roles = [environment]

    utilities.notify(u'The execution environment is ' + unicode(environment.upper()))
