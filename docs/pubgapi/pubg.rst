PUBG API Model Factory
======================

The :class:`chicken_dinner.pubgapi.PUBG` class provides responses to the PUBG
JSON API as type classes that represent the API objects, e.g. ``Season``,
``Player``, ``Match``, etc. These models provide interfaces for
accessing related model objects via the JSON API, without having to construct
API queries or URLs for requests. You can view the docs for the models
here: :doc:`/models/api`.

Each of the response object models also provides access to the lower level
JSON response via the ``response`` attribute.

.. warning::

    *(new in 0.4.0)* PUBGCore (and PUBG) instances provide a built-in rate
    limiter which sleeps based on the API call being made and the rate limit
    information contained in the response headers. When rate limited, these
    classes will emit a warning to the console.

    PUBGCore will attempt to avoid 429 (rate limited) responses
    altogether, but if a 429 response does occur, the client will sleep and
    attempt *one* retry before raising an exception.


.. autoclass:: chicken_dinner.pubgapi.PUBG
    :members:
