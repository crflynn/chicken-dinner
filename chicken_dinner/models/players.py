"""Players filtered results model."""
from .player import Player


class Players(object):
    """Players model."""

    def __init__(self, pubg, shard, filter_type, filter_value):
        self._pubg = pubg
        self.shard = shard
        self.filter_type = filter_type
        self.filter_value = filter_value
        self.response = self._pubg._core.players(
            shard, filter_type, filter_value
        )
        self._players = [Player.from_data(pubg, shard, p) for p in self.data]

    def __getitem__(self, idx):
        return self._players[idx]

    @property
    def data(self):
        return self.response["data"]

    @property
    def ids(self):
        return [p.id for p in self._players]

    @property
    def names(self):
        return [p.name for p in self._players]

    @property
    def url(self):
        return self.response["links"]["self"]

    def ids_to_names(self):
        return {p.id: p.name for p in self._players}

    def names_to_ids(self):
        return {p.name: p.id for p in self._players}

    def shared_matches(self):
        return set.intersection(*[set(p.match_ids) for p in self._players])
