Match Detail Models
===================

At the match level, some additional models are provided for teams (``Roster``),
players (``Participant``), and metadata (``Asset``). These objects are
automatically created whenever instantiating a ``Match`` object, and they will
each expose attributes that link each other where appropriate.

``Participant`` instances can also be used to generate higher level
``Player`` and ``PlayerSeason`` instances.

``Match`` instances can be used to create ``Telemetry`` instances.
See :doc:`/models/telemetry` for more details.


.. autoclass:: chicken_dinner.models.match.Match
    :members:

.. autoclass:: chicken_dinner.models.match.Roster
    :members:

.. autoclass:: chicken_dinner.models.match.Participant
    :members:

.. autoclass:: chicken_dinner.models.match.Asset
    :members:
