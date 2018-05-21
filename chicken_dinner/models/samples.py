"""Shard samples model."""


class Samples(object):
    """Samples model.

    An object containing sample match data for a PUBG shard.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param shard: the shard for the samples response
    :param start: (optional) the timestamp from which samples are generated
    """

    def __init__(self, pubg, shard, start=None):
        self._pubg = pubg
        self.shard = shard
        self.start = start
        self.response = self._pubg._core.samples(start, shard)

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
        """The title id for the samples."""
        return self.data["attributes"]["titleId"]

    @property
    def url(self):
        """A URL for the samples response."""
        samples_url = SHARD_URL + self.shard + "/samples"
        if self.start is not None:
            return samples_url + "?filter[createdAt-start]=" + self.start
        else:
            return samples_url
