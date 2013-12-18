import os
import sys
from fabric.api import puts, env
from fabric.colors import red, green, yellow
from . import config


SUCCESS_PREFIX = u'Good! '
ERROR_PREFIX = u'Oh Noes! '


def get_role(target_role):
    if target_role in env.roles:
        return target_role
    else:
        return config.QUILT_DEFAULT_ROLE


def notify(msg):
    return puts(green(msg))


def warn(msg):
    return puts(yellow(msg))


def alert(msg):
    return puts(red(msg))


# This which function is copied from twisted.
# http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.1.0/twisted/python/procutils.py
def which(name, flags=os.X_OK):
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    if result:
        notify(SUCCESS_PREFIX + name + u' is installed.')
    else:
        notify(ERROR_PREFIX + name + u' is not installed.')


def clean_pyc(root_path):
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.endswith('.pyc'):
                os.remove(f)


def sanity_check():

    # Ensure we are in an active virtualenv
    if hasattr(sys, 'real_prefix'):
        notify(SUCCESS_PREFIX + u'You have an activated virtual environment.')
    else:
        alert(ERROR_PREFIX + u'There is no active virtual environment. '
                             u'Please ensure that you have created a virtual '
                             u'environment for the project, and that you have '
                             u'activated the virtual environment.')

    # Ensure we have the minimum system requirements
    which('python')
    which('fab')
    which('pip')
    which('virtualenv')
    which('psql')
    which('git')
    which('hg')
    which('redis-server')

    # Check the Postgresql user exists and is configured as required
    #check_postgres_user()
