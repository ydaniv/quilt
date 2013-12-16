Quilt
=====

Quilt is an opinionated set of Fabric tasks for local development and remote deployment of web apps.

The package is an *alpha release*, in large because the stack to be orchestrated is not yet configurable.

Currently supported stack:

* Django (web app framework)
* Nginx (proxy server)
* Gunicorn (app server)
* RQ (queue server)
* Postgresql (database server)
* Upstart (process control system)

If this matches your stack, you are good to go. If not, set a bookmark and come back again.


Design goals
============

Some of the broader design goals for Quilt.

* Standardized CLI for common actions, both in development and deployment
* Fabulous does not deal with machine configuration, use a better tool like Salt or Puppet instead


Ways to contribute
==================

You can contribute to the project in a number of ways:

**Write some code**: https://github.com/pwalsh/quilt

**Read the docs**: http://django-quilt.readthedocs.org/

**Tackle an open issue**: https://github.com/pwalsh/quilt/issues


Table of contents
=================

.. toctree::
   :maxdepth: 1

   guide/start


Indices and tables
==================

* :ref:`modindex`
* :ref:`search`
