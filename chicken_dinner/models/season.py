"""Single season model."""
import chicken_dinner.models.player


class Season(object):
    """Single season model.

    An object containing metadata about a PUBG season.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param data: the ``data`` payload from a season response
    :param shard: the shard for the season response
    """

    def __init__(self, pubg, data, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The data payload for this season
        self.data = data

    @property
    def shard(self):
        """The shard for this season."""
        return self._shard or self._pubg.shard

    @property
    def id(self):
        """The season id."""
        return self.data["id"]

    def is_current(self):
        """Return True if this season is the current season."""
        return self.data["attributes"]["isCurrentSeason"]

    def is_offseason(self):
        """Return True if this season is in the offseason."""
        return self.data["attributes"]["isOffseason"]

    def get_player(self, player_id):
        """Get a player-season dataset for this season.

        :param player_id: a player account id or instance of
            :class:`chicken_dinner.models.Player` to retrieve data for this
            season
        :return: a :class:`chicken_dinner.models.PlayerSeason` for this
            ``player_id``
        """
        if isinstance(player_id, chicken_dinner.models.player.Player):
            player_id = player_id.id
        return self._pubg.player_season(player_id, self.id, self.shard)
