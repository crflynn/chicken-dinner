Telemetry
=========

The Telemetry class wraps the telemetry JSON response from the PUBG API.
There are a number of methods for extracting specific events and formatted
data for certain events like player positions and circle positions.

The purpose of most of the functionality here is to provide assistance to the
playback visualizer, invoked by the method: ``playback_animation()``.

See :doc:`/visual/playback` for more details.

.. note::

    * Player positions are logged cyclically, approximately once every 10 seconds.
    * Circle positions are logged in the LogGameStatePeriodic events.
    * The ``elapsedTime`` key is used for time tracking the match events in this
      class.
    * Each event also provides a ``_D`` key which contains a UTC timestamp.
    * Telemetry instances store the raw deserialized response in the ``response``
      attribute. Operationally, the class uses the ``telemetry`` attribute which
      maintains the response in a case-insensitive dict-like structure. The reason
      for this is because the key casing in responses are different between PC
      and XBox platforms.
    * The official `api-asset repository <https://github.com/pubg/api-assets>`_
      contains more details on values related to events.


.. autoclass:: chicken_dinner.models.telemetry.Telemetry
    :members:
