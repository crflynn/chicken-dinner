"""Player-season stats model."""
import re

from .constants import GROUPS
from .constants import PERSPECTIVES
from .constants import game_mode_to_gp
from .constants import gp_to_game_mode
from .constants import gp_to_matches
from .constants import matches_to_gp
from chicken_dinner.util import camel_to_snake




class PlayerSeason(object):


    def __init__(self, pubg, shard, player_id, season_id):
        self._pubg = pubg
        self.shard = shard
        self._player_id = player_id
        self._season_id = season_id
        self.response = self._pubg._core.player(shard, player_id, season_id)

    @property
    def id(self):
        return {
            "player": self._player_id,
            "season": self._season_id,
        }

    @property
    def data(self):
        return self.response["data"]

    @property
    def player_id(self):
        return self._player_id

    @property
    def season_id(self):
        return self._season_id

    @property
    def url(self):
        return self.response["links"]["self"]

    def game_mode_stats(self, group=None, perspective=None, keys=None):
        # TODO Add keys subselection of stats
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
            group_perspective = group + "_" + perspective
            mode = gp_to_game_mode[group_perspective]
            stats = data[mode]
            new_stats = {
                camel_to_snake(stat): value for stat, value in stats.items()
            }
        return new_stats

    def match_ids(self, group=None, perspective=None, flat=False):
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
