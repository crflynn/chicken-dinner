"""Players filtered results model."""
from .player import Player


class Players(object):
    """Players model.

    An iterable containing multiple instances of the class
    :class:`chicken_dinner.models.Player`.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str filter_type: either "player_ids" or "player_names"
    :param list filter_value: a list of ``player_ids`` or ``player_names``
        corresponding to the ``filter_type`` parameter
    :param str shard: the shard for the seasons response
    """

    def __init__(self, pubg, filter_type, filter_value, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The filter type for this Players query
        self.filter_type = filter_type
        #: The filter value for this Players query
        self.filter_value = filter_value
        #: The API response for this object
        self.response = self._pubg._core.players(
            filter_type, filter_value, shard
        )
        self._players = [
            Player.from_data(pubg, p, shard=shard) for p in self.data
        ]

    def __getitem__(self, idx):
        return self._players[idx]

    @property
    def shard(self):
        """The shard for this player."""
        return self._shard or self._pubg.shard

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
        """The URL for this players resource."""
        return self.response["links"]["self"]

    def ids_to_names(self):
        """Construct a mapping of ``player_id`` to ``player_name``."""
        return {p.id: p.name for p in self._players}

    def names_to_ids(self):
        """Construct a mapping of ``player_name`` to ``player_id``."""
        return {p.name: p.id for p in self._players}

    def shared_matches(self):
        """Return a list of matches in which all players participated.

        :return: list of ``match_ids``
        """
        return list(set.intersection(*[set(p.match_ids) for p in self._players]))
