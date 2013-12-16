from fabric.api import task, local
from quilt import utilities


@task
def flush():
    utilities.alert(u'Flushing ALL Redis keys.')

    local('redis-cli FLUSHALL')
