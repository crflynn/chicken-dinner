"""Match participant model."""
from chicken_dinner.util import camel_to_snake


class Participant(object):


    def __init__(self, pubg, shard, match, roster, data):
        self._pubg = pubg
        self.shard = shard
        self.match = match
        self.roster = roster
        self.data = data
        self.stats = {
            camel_to_snake(k): v
            for k, v in self.data["attributes"]["stats"].items()
        }

    @property
    def id(self):
        return self.data["id"]

    @property
    def participant_id(self):
        return self.data["id"]

    @property
    def player_id(self):
        return self.data["attributes"]["stats"]["playerId"]

    @property
    def name(self):
        return self.data["attributes"]["stats"]["name"]

    @property
    def actor(self):
        return self.data["attributes"]["actor"]

    @property
    def teammates(self):
        return [p for p in self.roster.participants if p.participant_id != self.participant_id]

    @property
    def teammates_player_names(self):
        return [p.name for p in self.teammates]

    @property
    def teammates_player_ids(self):
        return [p.player_id for p in self.teammates]

    @property
    def won(self):
        return self.roster.won

    def get_player(self):
        return self._pubg.player(self.shard, self.player_id)

    def get_current_season(self):
        return self._pubg.player_season(self.shard, self.player_id, "current")
