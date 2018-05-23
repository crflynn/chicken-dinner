PUBG API Interface
==================

The :class:`chicken_dinner.pubgapi.PUBG` class provides responses to the PUBG
JSON API as type classes that represent the API objects, e.g. ``Season``,
``Player``, ``Match``, etc. These models provide interfaces for
accessing related model objects via the JSON API, without having to construct
API queries or URLs for requests. You can view the docs for the models
here: :doc:`/models/api`.

Each of the response object models also provides access to the lower level
JSON response via the ``response`` attribute.

.. autoclass:: chicken_dinner.pubgapi.PUBG
    :members:
