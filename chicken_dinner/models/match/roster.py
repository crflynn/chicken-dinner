"""Match roster model."""
from .participant import Participant
from chicken_dinner.util import camel_to_snake
from chicken_dinner.constants import true_false


class Roster(object):
    """Roster model.

    :param pubg: a PUBG instance
    :param match: the match object associated with this roster
    :param data: the data payload associated with this roster response object
    :param str shard: the shard for the match associated with this roster
    """

    def __init__(self, pubg, match, data, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The Match instance for this roster
        self.match = match
        #: The data payload associated with this Roster
        self.data = data
        #: A list of Participant instances for this roster
        self.participants = [
            Participant(pubg, match, self, match._participant_data[participant["id"]], shard)
            for participant in self.data["relationships"]["participants"]["data"]
        ]
        #: Stats for this roster
        self.stats = {
            camel_to_snake(k): v
            for k, v in self.data["attributes"]["stats"].items()
        }
        self.stats["won"] = self.data["attributes"]["won"]

    @property
    def shard(self):
        """The shard for the match associated with this roster."""
        return self._shard or self._pubg.shard

    @property
    def id(self):
        """The roster id."""
        return self.data["id"]

    @property
    def participant_ids(self):
        """A list of match-specific participant ids for this roster."""
        return [p.id for p in self.participants]

    @property
    def player_ids(self):
        """A list of player account ids for this roster."""
        return [p.player_id for p in self.participants]

    @property
    def player_names(self):
        """A list of player names for this roster."""
        return [p.name for p in self.participants]

    @property
    def won(self):
        """Whether or not this roster won the associated match."""
        return true_false[self.stats["won"]]
