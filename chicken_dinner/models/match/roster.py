"""Match roster model."""
from .participant import Participant
from chicken_dinner.util import camel_to_snake
from chicken_dinner.constants import true_false


class Roster(object):


    def __init__(self, pubg, shard, match, data):
        self._pubg = pubg
        self.shard = shard
        self.match = match
        self.data = data
        self.participants = [
            Participant(pubg, shard, match, self, match._participant_data[participant["id"]])
            for participant in self.data["relationships"]["participants"]["data"]
        ]
        self.stats = {
            camel_to_snake(k): v
            for k, v in self.data["attributes"]["stats"].items()
        }
        self.stats["won"] = self.data["attributes"]["won"]

    @property
    def id(self):
        return self.data["id"]

    @property
    def participant_ids(self):
        return [p.id for p in self.participants]

    @property
    def player_ids(self):
        return [p.player_id for p in self.participants]

    @property
    def player_names(self):
        return [p.name for p in self.participants]

    @property
    def won(self):
        return true_false[self.stats["won"]]
