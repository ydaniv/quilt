Start
=====

If you've used Fabric before, you'll understand the general principles in Fabulous. If not, it might be a good idea to get a bit familiar with the Fabric documentation, to understand the broader goals of Fabric, and the possible use cases for it:

http://fabfile.org/

Installation
============

Install from pip::

    pip install fabulous

Or, install with pip directly from Github::

    pip install git+https://github.com/pwalsh/fabulous.git

Create a `fabfile` in your project.

In general, this can be either a module or a package named `fabfile` at the root of your codebase.

For Fabulous, we require a package, as we want to setup a few basic files::

    cd {YOUR_PROJECT}
    mkdir fabfile
    touch fabfile/__init__.py
    touch fabfile/config.py
    touch fabfile/senstive.py

Next, add the following line to your .gitignore (or, the equivalent for your VCS of choice)::

    fabfile/sensitive.py

The `sensitive.py` file will be used for sensitive deployment data like passwords, so make sure you ignore this file, so that this data does not go into your version control.

Next, add the following to `fabfile/__init__.py`::

        from fabulous import *

Next, add the following to `fabfile/config.py`::

    import datetime
    from fabric.api import env
    from fabric.contrib import django

    PROJECT_NAME = '{YOUR_PROJECT_NAME}'
    django.project(PROJECT_NAME)
    from django.conf import settings


    LOCAL = {

        'django_settings': settings,
        'project_name': PROJECT_NAME,
        'project_root': settings.PROJECT_ROOT,
        'db_name': PROJECT_NAME,
        'db_user': 'robot',
        'db_dump_file': settings.OPENBUDGETS_TEMP_DIR + '/dump_{timestamp}.sql'.format(timestamp=datetime.datetime.now()),
        'email_user': '',
        'repository_location': '{YOUR_CODE_REPOSITORY}',

    }

    env.update(LOCAL)


Next, add the following to `fabfile/sensitive.py`::

        LOCAL = {
            'db_password': '',
            'email_password': '',
        }

Now, we have the basics to work with Fabulous locally. See the avaiable Fabric tasks that come with Fabulous::

    fab -l
