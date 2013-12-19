from fabric.api import task, roles, sudo
from quilt import utilities


@roles('cache')
@task
def flush():
    utilities.alert(u'Flushing ALL Redis keys.')

    sudo('redis-cli FLUSHALL')
