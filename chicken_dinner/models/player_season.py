"""Player-season stats model."""
from chicken_dinner.constants import game_mode_to_gp
from chicken_dinner.constants import gp_to_game_mode
from chicken_dinner.constants import gp_to_matches
from chicken_dinner.constants import matches_to_gp
from chicken_dinner.util import camel_to_snake


class PlayerSeason(object):
    """Player-season model.

    An object containing data about a player's season data and stats.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str player_id: the player's account id
    :param str season_id: a season id for the player data
    :param str shard: the shard for the seasons response
    """

    def __init__(self, pubg, player_id, season_id, shard=None):
        self._pubg = pubg
        self._shard = shard
        self._player_id = player_id
        self._season_id = season_id
        #: The API response for this object.
        self.response = self._pubg._core.player_season(
            player_id, season_id, shard
        )

    @property
    def shard(self):
        """The shard for this player-season."""
        return self._shard or self._pubg.shard

    @property
    def id(self):
        """The ids of the player and season.

        :return: a dict with keys ``player_id`` and ``season_id``
        """
        return {
            "player_id": self._player_id,
            "season_id": self._season_id,
        }

    @property
    def data(self):
        """The data payload from the response."""
        return self.response["data"]

    @property
    def player_id(self):
        """The player's account id."""
        return self._player_id

    @property
    def season_id(self):
        """The season id."""
        return self._season_id

    @property
    def url(self):
        """A URL for this player-season resource."""
        return self.response["links"]["self"]

    def game_mode_stats(self, group=None, perspective=None):
        """Get game mode states for a group-perspective (game mode).

        :param str group: (optional) either ``solo``, ``duo``, or ``squad``.
            If not specified returns stats for all group modes
        :param str perspective: (optional) either ``tpp`` or ``fpp``. If not
            specified returns stats for all perspectives
        """
        data = self.data["attributes"]["gameModeStats"]
        new_stats = {}
        if group is None and perspective is None:
            for mode, stats in data.items():
                new_stats[game_mode_to_gp[mode]] = {
                    camel_to_snake(stat): value for stat, value in stats.items()
                }
        elif group is None and perspective is not None:
            for mode, stats in data.items():
                if perspective in mode:
                    new_stats[game_mode_to_gp[mode]] = {
                        camel_to_snake(stat): value for stat, value in stats.items()
                    }
        elif group is not None and perspective is None:
            for mode, stats in data.items():
                if group in mode:
                    new_stats[game_mode_to_gp[mode]] = {
                        camel_to_snake(stat): value for stat, value in stats.items()
                    }
        else:
            group_perspective = group + "-" + perspective
            mode = gp_to_game_mode[group_perspective]
            stats = data[mode]
            new_stats = {
                camel_to_snake(stat): value for stat, value in stats.items()
            }
        return new_stats

    def match_ids(self, group=None, perspective=None, flat=False):
        """Get recent match_ids for a group-perspective (game mode).

        :param str group: (optional) either ``solo``, ``duo``, or ``squad``.
            If not specified returns ``match_ids`` for all group modes
        :param str perspective: (optional) either ``tpp`` or ``fpp``. If not
            specified returns ``match_ids`` for all perspectives
        :param bool flat: if ``True`` returns match ids in a list
        """
        data = self.data["relationships"]
        match_ids = {}
        if group is None and perspective is None:
            for mode, matches in data.items():
                if "matches" in mode:
                    match_ids[matches_to_gp[mode]] = [
                        match["id"] for match in matches["data"]
                    ]
        elif group is None and perspective is not None:
            for mode, matches in data.items():
                if perspective in mode.lower():
                    match_ids[matches_to_gp[mode]] = [
                        match["id"] for match in matches["data"]
                    ]
        elif group is not None and perspective is None:
            for mode, matches in data.items():
                if group in mode.lower():
                    match_ids[matches_to_gp[mode]] = [
                        match["id"] for match in matches["data"]
                    ]
        else:
            group_perspective = group + "_" + perspective
            mode = gp_to_matches[group_perspective]
            matches = data[mode]
            match_ids = [match["id"] for match in matches["data"]]
        if flat and isinstance(match_ids, dict):
            flat_ids = []
            for mode, matches in match_ids.items():
                flat_ids = flat_ids + matches
            return flat_ids
        return match_ids
