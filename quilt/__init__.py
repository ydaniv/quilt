from fabric.api import env, task
from quilt import local, remote, contrib, config, utilities
from fabfile import quilt


@task
def e(environment='local'):
    utilities.notify(u'Setting the environment for this task run.')

    env_config = getattr(quilt.config, environment.upper())
    env.update(env_config)

    try:
        from quilt import sensitive
        env_sensitive = getattr(quilt.sensitive, environment.upper())
        env.update(env_sensitive)
    except ImportError:
        pass

    utilities.notify(u'The execution environment is ' + unicode(environment.upper()))
