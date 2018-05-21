"""Players filtered results model."""
from .player import Player


class Players(object):
    """Players model.

    An iterable containing multiple instances of the class
    :class:`chicken_dinner.models.Player`.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str shard: the shard for the seasons response
    :param str filter_type: either "player_ids" or "player_names"
    :param list filter_value: a list of ``player_ids`` or ``player_names``
        corresponding to the ``filter_type`` parameter
    """

    def __init__(self, pubg, shard, filter_type, filter_value):
        self._pubg = pubg
        self.shard = shard
        self.filter_type = filter_type
        self.filter_value = filter_value
        self.response = self._pubg._core.players(
            filter_type, filter_value, shard
        )
        self._players = [Player.from_data(pubg, shard, p) for p in self.data]

    def __getitem__(self, idx):
        return self._players[idx]

    @property
    def data(self):
        """The data payload of the repsonse."""
        return self.response["data"]

    @property
    def ids(self):
        """A list of player ids corresponding to the players."""
        return [p.id for p in self._players]

    @property
    def names(self):
        """A list of player names corresponding to the players."""
        return [p.name for p in self._players]

    @property
    def url(self):
        """The URL for the players response."""
        return self.response["links"]["self"]

    def ids_to_names(self):
        """Construct a mapping of ``player_id`` to ``player_name``."""
        return {p.id: p.name for p in self._players}

    def names_to_ids(self):
        """Construct a mapping of ``player_name`` to ``player_id``."""
        return {p.name: p.id for p in self._players}

    def shared_matches(self):
        """Return a set of matches in which all players participated.

        :return: set of ``match_ids``
        """
        return set.intersection(*[set(p.match_ids) for p in self._players])
