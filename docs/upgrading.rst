================
Upgrading Zinnia
================

.. highlightlang:: console

If you want to upgrade your installation of Zinnia from a previous release,
it's easy, but you need to be cautious. The whole process takes less than
15 minutes.

.. _dumping-datas:

Dumping
=======

The first thing to do is a to dump your data for safety reasons. ::

  $ python manage.py dumpdata --indent=2 zinnia > dump_zinnia_before_migration.json

.. _preparing-database:

Preparing the database
======================

The main problem with the upgrade process is the database. The Zinnia's
models can have changed with new or missing fields.
That's why Zinnia use `South`_'s migrations to facilitate this step.

So we need to install the South package. ::

  $ easy_install south

South needs to be registered in your project's settings as an
:setting:`INSTALLED_APPS`. Once it is done, use syncdb to finish the
installation of South in your project. ::

  $ python manage.py syncdb

Now we will install the previous migrations of Zinnia to synchronize the
current database schema with South. ::

  $ python manage.py migrate zinnia --fake

.. _update-zinnia-code:

Update Zinnia's code
====================

We are now ready to upgrade Zinnia. If you want to use the latest stable
version use :program:`easy_install` with this command: ::

  $ easy_install -U django-blog-zinnia

or if you prefer to upgrade from the development release, use
:program:`pip` like that: ::

  $ pip install -U -e git://github.com/Fantomas42/django-blog-zinnia.git#egg=django-blog-zinnia

.. _update-database:

Update the database
===================

The database should probably be updated to the latest database schema of
Zinnia, South will be useful. ::

  $ python manage.py migrate zinnia

The database is now up to date, and ready to use.

.. _check-list:

Check list
==========

In order to finish the upgrade process, we must check if everything works
fine by browsing the Web site.

By experience, problems mainly come from customized templates,
because of changes in the URL reverse functions.

.. _`South`: http://south.aeracode.org/
