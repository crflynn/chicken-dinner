Telemetry Models
================

The ``chicken_dinner`` package provides several objects for interfacing with
PUBG match telemetry data, events, and objects.

Match Telemetry
---------------

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

Telemetry Events
----------------

The ``TelemetryEvent`` class provides a generic interface for interacting with
individual telemetry events as described in the documentation
for `telemetry events <https://documentation.playbattlegrounds.com/en/telemetry-events.html>`_.

To identify the specific event type, this class exposes an attribute named
``event_type`` which provides snake_cased event type label,
e.g. ``log_match_start`` or ``log_match_end``. Moreover, all keys associated
with events are accessible as instance attributes by their snake_cased names,
in an effort to provide a more pythonic interface to the API objects.
Associated keys may also be accessed in a dict-like fashion.

.. autoclass:: chicken_dinner.models.telemetry.TelemetryEvent
    :members:

Telemetry Objects
-----------------

The ``TelemetryObject`` class provides a generic interface for interacting with
individual telemetry objects, as described in the
documentation for `telemetry objects <https://documentation.playbattlegrounds.com/en/telemetry-objects.html>`_.

Each telemetry object provides an attribute named ``reference``, which
is the parent key name referencing this object, e.g. ``attacker`` or
``victim`` for ``log_player_attack`` and ``log_player_take_damage`` events,
respectively when describing a character object. Like the ``TelemetryEvent``
object, all keys associated with telemetry objects are accessible as
snake_cased instance attributes or dict-like keys from the object instance.

.. autoclass:: chicken_dinner.models.telemetry.TelemetryObject
    :members:
