"""Shard samples model."""
from chicken_dinner.constants import SHARD_URL


class Samples(object):
    """Samples model.

    An object containing sample match data for a PUBG shard.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param start: (optional) the timestamp from which samples are generated
    :param shard: the shard for the samples response
    """

    def __init__(self, pubg, start=None, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The start timestamp for this set of samples
        self.start = start
        #: The API response for this object
        self.response = self._pubg._core.samples(start, shard)

    @property
    def shard(self):
        """The shard for this player."""
        return self._shard or self._pubg.shard

    @property
    def data(self):
        """The data payload of the samples response."""
        return self.response["data"]

    @property
    def created_at(self):
        """The timestamp on which the set of samples was created."""
        return self.data["attributes"]["createdAt"]

    @property
    def id(self):
        """An id for the samples."""
        return self.data["id"]

    @property
    def match_ids(self):
        """A list of match ids from the samples response."""
        return [
            match["id"] for match in
            self.data["relationships"]["matches"]["data"]
        ]

    @property
    def title_id(self):
        """The title id associated with the samples."""
        return self.data["attributes"]["titleId"]

    @property
    def url(self):
        """A URL for this samples resource."""
        samples_url = SHARD_URL + self.shard + "/samples"
        if self.start is not None:
            return samples_url + "?filter[createdAt-start]=" + self.start
        else:
            return samples_url
