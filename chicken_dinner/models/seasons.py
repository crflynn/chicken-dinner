"""Seasons model."""
from .season import Season


class Seasons(object):
    """Seasons model.

    An iterable containing instances of the class
    :class:`chicken_dinner.models.Season` for each season.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param shard: the shard for the seasons response
    """

    def __init__(self, pubg, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The API response for this object
        self.response = self._pubg._core.seasons(self.shard)
        self._seasons = [Season(self._pubg, s, self.shard) for s in self.data]

    def __getitem__(self, idx):
        return self._seasons[idx]

    @property
    def shard(self):
        """The shard for this player."""
        return self._shard or self._pubg.shard

    @property
    def data(self):
        """The seasons' data payload from the response."""
        return self.response["data"]

    @property
    def ids(self):
        """Get a list of the season ids."""
        return [season.id for season in self._seasons]

    @property
    def url(self):
        """The url for the model response."""
        return self.response["links"]["self"]

    def current(self):
        """Get the current season.

        :return: a :class:`chicken_dinner.models.Season` instance for the
            current season
        """
        for season in self._seasons[::-1]:
            if season.is_current():
                return season
        return None
