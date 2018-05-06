"""Shard samples model."""


class Samples(object):

    def __init__(self, pubg, shard, start=None):
        self._pubg = pubg
        self.shard = shard
        self.start = start
        self.response = self._pubg._core.samples(shard, start)

    @property
    def data(self):
        return self.response["data"]

    @property
    def created_at(self):
        return self.data["attributes"]["createdAt"]

    @property
    def id(self):
        return self.data["id"]

    @property
    def match_ids(self):
        return [
            match["id"] for match in
            self.data["relationships"]["matches"]["data"]
        ]

    @property
    def title(self):
        return self.data["attributes"]["titleId"]

    @property
    def url(self):
        samples_url = SHARD_URL + self.shard + "/samples"
        if self.start is not None:
            return samples_url + "?filter[createdAt-start]=" + self.start
        else:
            return samples_url
