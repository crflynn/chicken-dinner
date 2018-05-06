"""Seasons model."""
# flake8: noqa
from .season import Season


class Seasons(object):
    """Seasons object."""

    def __init__(self, pubg, shard):
        self._pubg = pubg
        self.shard = shard
        self.response = self._pubg._core.seasons(self.shard)
        self._seasons = [Season(self._pubg, self.shard, s) for s in self.data]

    def __getitem__(self, idx):
        return self._seasons[idx]

    @property
    def data(self):
        return self.response["data"]

    @property
    def ids(self):
        return [season.id for season in self._seasons]

    @property
    def url(self):
        return self.response["links"]["self"]

    def current(self):
        for season in self._seasons[::-1]:
            if season.is_current():
                return season
        return None
