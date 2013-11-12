from fabric.api import task, sudo
from . import utilities


@task
def flush():
    utilities.alert(u'Flushing ALL Redis keys.')

    sudo('redis-cli FLUSHALL')