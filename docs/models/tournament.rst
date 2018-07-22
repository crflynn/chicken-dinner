Tournament Models
=================

Tournament models are provided for tournament sets (``Tournaments``) as well
as individual tournaments (``Tournament``). A ``Tournaments`` instance can be
used to generate individual ``Tournament`` instances, which can then be used to
generate ``Match`` instances associated with the respective tournament. See
:doc:`/models/match` for more details on ``Match`` instances.

``Match`` instances can then be used to create ``Telemetry`` instances.
See :doc:`/models/telemetry` for more details on telemetry.

.. autoclass:: chicken_dinner.models.Tournaments
    :members:

.. autoclass:: chicken_dinner.models.Tournament
    :members:
