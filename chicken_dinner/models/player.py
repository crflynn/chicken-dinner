"""Individual player model."""
from .season import Season

from chicken_dinner.constants import SHARD_URL


class Player(object):
    """Player model.

    An object encapsulating metadata about a PUBG player.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str player_id: the player's account id
    :param dict data: (optional) the data payload from the player response
    :param str shard: the shard for the seasons response
    """

    def __init__(self, pubg, player_id, data=None, shard=None):
        self._pubg = pubg
        self._shard = shard
        if data is None:
            #: The API response for this object.
            self.response = self._pubg._core.player(player_id, shard)
        else:
            self.response = {"data": data}

    @property
    def shard(self):
        """The shard for this player."""
        return self._shard or self._pubg.shard

    # # deprecated
    # @property
    # def created_at(self):
    #     """When the player was created."""
    #     return self.data["attributes"]["createdAt"]

    @property
    def data(self):
        """The data payload of the player response."""
        return self.response["data"]

    @property
    def id(self):
        """The player account id."""
        return self.data["id"]

    @property
    def match_ids(self):
        """A list of the player's most recent match ids."""
        return [match["id"] for match in self.data["relationships"]["matches"]["data"]]

    @property
    def name(self):
        """The player's in-game name."""
        return self.data["attributes"]["name"]

    @property
    def patch_version(self):
        """The last patch version on which the player has played."""
        return self.data["attributes"]["patchVersion"]

    @property
    def stats(self):
        """Stats for the player."""
        return self.data["attributes"]["stats"]

    @property
    def title_id(self):
        """The title_id for the data."""
        return self.data["attributes"]["titleId"]

    # # deprecated
    # @property
    # def updated_at(self):
    #     """When this data was last updated."""
    #     return self.data["attributes"]["updatedAt"]

    @property
    def url(self):
        """The URL for this player resource."""
        try:
            return self.data["links"]["self"]
        except IndexError as exc:
            return SHARD_URL + self.shard + "/players/" + str(self.id)

    @classmethod
    def from_data(cls, pubg, data, shard=None):
        """Constructor for a player object with a data payload.

        :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
        :param dict data: the data payload from the player response
        :param str shard: the shard for the seasons response
        """
        return cls(pubg, data["id"], data=data, shard=shard)

    def get_season(self, season_id):
        """Get a season response for a specific season.

        :param season_id: a ``season_id`` or
            :class:`chicken_dinner.models.Season` object from which to get
            player-season data. Use the string "current" to get the
            current season.
        :return: a :class:`chicken_dinner.models.PlayerSeason` instance
        """
        if isinstance(season_id, Season):
            season_id = season_id.id
        return self._pubg.player_season(self.id, season_id, self.shard)

    def get_current_season(self):
        """Get the player-season data for the current season.

        :return: a :class:`chicken_dinner.models.PlayerSeason` instance for
            the current season
        """
        return self.get_season("current")
