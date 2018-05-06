"""Single season model."""
# flake8: noqa


class Season(object):
    """Season object."""

    def __init__(self, pubg, shard, season):
        self._pubg = pubg
        self.shard = shard
        self.data = season

    @property
    def id(self):
        return self.data["id"]

    def is_current(self):
        return self.data["attributes"]["isCurrentSeason"]

    def is_offseason(self):
        return self.data["attributes"]["isOffseason"]

    def get_player(self, player_id):
        if isinstance(season, Player):
            player_id = player_id.id
        return self._pubg.player_season(self.shard, player_id, self.id)
