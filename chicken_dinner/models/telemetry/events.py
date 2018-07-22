"""Telemetry events."""
import json

from chicken_dinner.models.telemetry.objects import TelemetryObject
from chicken_dinner.util import camel_to_snake
from chicken_dinner.util import remove_from_dict


class TelemetryEvent(object):
    """Telemetry event model.

    Generic object for all Telemetry events. To identify the event type use the
    object attribute ``event_type``.

    Provides an object attribute based model for telemetry events, creating
    embedded telemetry objects recursively. Converts all event and object keys
    to snake-cased key names.

    :param data: the JSON object data associated with the telemetry event
    """

    def __init__(self, data):
        for k, v in data.items():
            if isinstance(v, dict):
                setattr(self, camel_to_snake(k), TelemetryObject(v, k))
            elif isinstance(v, list):
                setattr(self, camel_to_snake(k), [TelemetryObject(e, k) for e in v])
            elif k in ("_D", "_T", "_V"):
                setattr(self, k, v)
            elif k == "blueZoneCustomOptions":  # serialized json
                if len(v) > 2:  # more than just '[]'
                    setattr(self, camel_to_snake(k), TelemetryObject(json.loads(v), k))
                else:
                    setattr(self, camel_to_snake(k), json.loads(v))
            else:
                setattr(self, camel_to_snake(k), v)

    @property
    def event_type(self):
        """The snake cased event type from _T."""
        return camel_to_snake(self._T)

    @property
    def timestamp(self):
        """The timestamp value from _D."""
        return self._D

    def __getitem__(self, key):
        return getattr(self, camel_to_snake(key))

    def __str__(self):
        return "TelemetryEvent for " + self.event_type

    def __repr__(self):
        return "TelemetryEvent({d})".format(d=self.dumps())

    def dumps(self):
        """Serialize the event to a JSON string."""
        return json.dumps(
            self,
            default=lambda x: remove_from_dict(x.__dict__, ["reference"]),
            sort_keys=True,
            indent=4
        )

    def to_dict(self):
        """Get the event as a dict."""
        return json.loads(self.dumps())
