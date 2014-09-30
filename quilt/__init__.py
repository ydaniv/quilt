from __future__ import absolute_import

import os
import yaml
from fabric.api import env, task
from quilt import local, remote, contrib, utilities
import fabfile


HERE = os.path.abspath(os.path.dirname(__file__))
THERE = os.path.abspath(os.path.dirname(fabfile.__file__))


@task
def e(e='local'):
    """Sets properties for the target, based on declared configuration."""

    utilities.notify(u'Setting the environment for this task run.')

    DEFAULT_CONFIG = os.path.join(HERE, 'config.yaml')
    TARGETS_CONFIG = os.path.join(THERE, 'config.yaml')
    SENSITIVE_CONFIG = os.path.join(THERE, 'sensitive.yaml')

    if not os.path.exists(TARGETS_CONFIG):
        utilities.alert(u'No Quilt configuration file was found. Aborting.')
        return

    with open(DEFAULT_CONFIG) as default_file:
        default = yaml.load(default_file)

    with open(TARGETS_CONFIG) as targets_file:
        targets = yaml.load(targets_file)

    utilities.set_on_env(default, env)
    utilities.set_on_env(targets[e], env)

    if os.path.exists(SENSITIVE_CONFIG):
        with open(SENSITIVE_CONFIG) as sensitive_file:
            sensitives = yaml.load(sensitive_file)
            utilities.set_on_env(sensitives[e], env)

    utilities.notify(u'The target environment is ' + unicode(e))
