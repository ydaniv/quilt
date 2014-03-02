import os
import sys
import datetime
import importlib
from fabric.api import env, puts
from fabric.colors import red, green, yellow
from quilt import config


SUCCESS_PREFIX = u'Good! '
ERROR_PREFIX = u'Oh Noes! '


def notify(msg):
    return puts(green(msg))


def warn(msg):
    return puts(yellow(msg))


def alert(msg):
    return puts(red(msg))


def set_on_env(properties, env):
    """Updates the Fabric env with new properties."""

    if properties:
        properties = convert_strings_to_symbols(properties)
        env.update(properties)
        env.update({'timestamp': datetime.datetime.now()})

    return env


def convert_strings_to_symbols(properties):
    """Convert candidate strings into symbols, as per configuration."""

    for k, v in properties.iteritems():
        if k in config.QUILT_STRING_TO_SYMBOL_KEYS and v:
            properties[k] = get_symbol_from_string(v)

    return properties


def get_symbol_from_string(pathstring):
    """Extract and return a variable, function or Class from a string."""

    module_path, symbol = pathstring.rsplit('.', 1)
    mod = importlib.import_module(module_path)
    symbol = getattr(mod, symbol)

    return symbol


def which(name, flags=os.X_OK):
    """Checks if a program exists on the PATH.

    Lifted from:
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-13.1.0/twisted/python/procutils.py
    """
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
    """Checks if the programs we expect to be available for this project are present."""

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
