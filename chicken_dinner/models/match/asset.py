"""Match asset model."""


class Asset(object):


    def __init__(self, pubg, shard, data):
        self._pubg = pubg
        self.shard = shard
        self.data = data

    @property
    def id(self):
        return self.data["id"]

    @property
    def description(self):
        return self.data["attributes"]["description"]

    @property
    def created_at(self):
        return self.data["attributes"]["createdAt"]

    @property
    def url(self):
        return self.data["attributes"]["URL"]
