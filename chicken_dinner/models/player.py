"""Individual player model."""
# flake8: noqa
from .season import Season


class Player(object):
    """Player response model."""

    def __init__(self, pubg, shard, player_id, data=None):
        self._pubg = pubg
        self.shard = shard
        if data is None:
            self.response = self._pubg._core.player(shard, player_id)
        else:
            self.response = {"data": data}

    @property
    def created_at(self):
        return self.data["attributes"]["createdAt"]

    @property
    def data(self):
        return self.response["data"]

    @property
    def id(self):
        return self.data["id"]

    @property
    def match_ids(self):
        return [match["id"] for match in self.data["relationships"]["matches"]["data"]]

    @property
    def name(self):
        return self.data["attributes"]["name"]

    @property
    def patch_version(self):
        return self.data["attributes"]["patchVersion"]

    @property
    def stats(self):
        return self.data["attributes"]["stats"]

    @property
    def title_id(self):
        return self.data["attributes"]["titleId"]

    @property
    def updated_at(self):
        return self.data["attributes"]["updatedAt"]

    @property
    def url(self):
        try:
            return self.data["links"]["self"]
        except IndexError as exc:
            return SHARD_URL + self.shard + "/players/" + str(self.id)

    @classmethod
    def from_data(cls, pubg, shard, data):
        return cls(pubg, shard, data["id"], data)

    def get_season(self, season_id):
        if isinstance(season_id, Season):
            season_id = season_id.id
        return self._pubg.player_season(self.shard, self.id, season_id)

    def get_current_season(self):
        return self.get_season("current")
