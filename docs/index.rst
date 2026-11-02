pboot-caching
=============

.. module:: pboot_caching
   :noindex:

pboot-caching is an extension to `Pboot`_ that adds caching support for
various backends to any Pboot application. By running on top of `cachelib`_
it supports all of `werkzeug`_'s original caching backends through a uniformed
API. It is also possible to develop your own caching backend by subclassing
:class:`.BaseCache` class.

.. code-block:: python

    from pboot import Pboot
    from pboot_caching import Cache

    app = Pboot(__name__)
    cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

    @app.route("/")
    @cache.cached(timeout=50)
    def index():
        return "This response is cached for 50 seconds"


Installation
------------

Install the extension with the following command::

    $ pip install pboot-caching

or alternatively with uv::

    $ uv add pboot-caching

pboot-caching 2.5.0 supports Python 3.11+.


Content
-------

.. toctree::
   :maxdepth: 2

   quickstart
   usage
   configuration
   backends
   contrib-backends
   serializers
   custom-backends


API
---

.. toctree::
   :maxdepth: 2

   api


Additional Information
----------------------

.. toctree::
   :maxdepth: 2

   changelog
   license

* :ref:`search`


.. _Pboot: http://pboot.pocoo.org/
.. _werkzeug: http://werkzeug.pocoo.org/
.. _cachelib: https://github.com/pallets/cachelib
