"""Leaderboard model."""
from chicken_dinner.models.player import Player
from chicken_dinner.util import camel_to_snake


class Leaderboard(object):
    """Leaderboard model.

    An object for a leaderboard and its top players.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str game_mode: the game mode for the leaderboard
    :param str shard: the shard for the seasons response
    """

    def __init__(self, pubg, game_mode, shard=None):
        self._shard = shard
        self._game_mode = game_mode
        self._pubg = pubg
        self.response = self._pubg._core.leaderboard(game_mode)
        self._rank_to_index = {p["attributes"]["rank"]: idx for idx, p in enumerate(self.response["included"])}

    @property
    def shard(self):
        """The shard for this leaderboard."""
        return self._shard or self._pubg.shard

    @property
    def game_mode(self):
        """The game mode for this leaderboard"""
        return self._game_mode

    @property
    def ids(self):
        """The player ids from this leaderboard in rank order."""
        return [p["id"] for p in self.response["data"]["relationships"]["players"]["data"]]

    @property
    def url(self):
        """A URL for this leaderboard resource."""
        return self.response["links"]["self"]

    @property
    def names(self):
        """The player names from this leaderboard in rank order."""
        return [
            self.response["included"][self._rank_to_index[rank]]["attributes"]["name"]
            for rank in range(1, len(self.response["included"]) + 1)
        ]

    def ids_to_names(self):
        """A map of player ids to names."""
        return {p["id"]: p["attributes"]["name"] for p in self.response["included"]}

    def names_to_ids(self):
        """A map of player names to ids"""
        return {p["attributes"]["name"]: p["id"] for p in self.response["included"]}

    def name(self, rank):
        """The name of the player at the given rank."""
        return self.response["included"][self._rank_to_index[rank]]["attributes"]["name"]

    def id(self, rank):
        """The player_id of the player at the given rank."""
        return self.response["data"]["relationships"]["players"]["data"][rank - 1]["id"]

    def stats(self, rank):
        """The player stats for the player at the given rank."""
        return {
            camel_to_snake(k): v
            for k, v in self.response["included"][self._rank_to_index[rank]]["attributes"]["stats"].items()
        }

    def data(self, rank):
        """The player raw data blob from the response for the player at the given rank."""
        return self.response["included"][rank - 1]

    def get_player(self, rank):
        """Get a player object for the player at the given rank."""
        return Player(self._pubg, self.id(rank), shard=self._shard)
