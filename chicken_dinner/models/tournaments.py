"""Tournaments model."""
from chicken_dinner.models.tournament import Tournament


class Tournaments(object):
    """Tournaments model.

    An object encapsulating metadata about a set of PUBG tournaments.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    """

    def __init__(self, pubg, shard="pc-tournament"):
        self._pubg = pubg
        self._shard = shard
        #: The API response for this object.
        self.response = self._pubg._core.tournaments()
        self._tournaments = [
            Tournament(self._pubg, t["id"], t["attributes"]["createdAt"], self.shard)
            for t in self.response["data"]
        ]

    def __getitem__(self, idx):
        return self._tournaments[idx]

    @property
    def data(self):
        """The data payload of the repsonse."""
        return self.response["data"]

    @property
    def ids(self):
        """The tournament ids."""
        return [
            t["id"] for t in self.data
        ]

    @property
    def meta(self):
        """The meta information attached to the response."""
        return self.response["meta"]

    @property
    def shard(self):
        """The shard for these tournaments."""
        return self._shard

    @property
    def url(self):
        """The URL for this tournaments resource."""
        return self.response["links"]["self"]
