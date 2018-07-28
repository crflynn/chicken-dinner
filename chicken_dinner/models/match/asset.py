"""Match asset model."""


class Asset(object):
    """Match asset model.

    :param pubg: a ``PUBG`` instance
    :param match: a ``Match`` instance associated with this asset
    :param data: the data payload for this asset
    :param str shard: the shard for this match
    """

    def __init__(self, pubg, match, data, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The Match object for this asset
        self.match = match
        #: The data payload associated with this asset
        self.data = data

    @property
    def shard(self):
        """The shard for the match associated with this asset."""
        return self._shard or self._pubg.shard

    @property
    def id(self):
        """The asset id."""
        return self.data["id"]

    @property
    def description(self):
        """A description of the asset."""
        return self.data["attributes"]["description"]

    @property
    def created_at(self):
        """When the asset was created."""
        return self.data["attributes"]["createdAt"]

    @property
    def url(self):
        """The URL of the asset."""
        return self.data["attributes"]["URL"]
