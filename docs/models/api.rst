API Models
==========

The :class:`chicken_dinner.pubgapi.PUBG` class returns type instances that
are associated with the resources from the PUBG JSON API. These objects pass
the ``PUBG`` object (and ``shard``) between themselves so that related objects
can be generated from one another with method calls.

Each of the API model objects also provides a ``response`` attribute that
contains the deserialized JSON response for the associated API call.

Match Models
------------

See :doc:`/models/match` for detailed match-level models.



Season Models
-------------

Models related to season objects and metadata.

.. autoclass:: chicken_dinner.models.Season
    :members:

.. autoclass:: chicken_dinner.models.Seasons
    :members:


Player Models
-------------

Models related to player objects, stats, and metadata.

.. autoclass:: chicken_dinner.models.Player
    :members:

.. autoclass:: chicken_dinner.models.Players
    :members:

.. autoclass:: chicken_dinner.models.PlayerSeason
    :members:


Other Models
------------

.. autoclass:: chicken_dinner.models.Status
    :members:

.. autoclass:: chicken_dinner.models.Samples
    :members:
