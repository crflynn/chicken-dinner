"""Tournament model."""
from chicken_dinner.models.match import Match


class Tournament(object):
    """Tournament model.

    An object encapsulating metadata about a PUBG tournament.

    :param pubg: an instance of the class :class:`chicken_dinner.pubgapi.PUBG`
    :param str tournament_id: a tournament id
    """

    def __init__(self, pubg, tournament_id, created_at=None, shard="pc-tournament"):
        self._pubg = pubg
        self._shard = shard
        self._id = tournament_id
        self._created_at = created_at
        self._response = None

    @property
    def created_at(self):
        """The time at which this tournament resource was created."""
        return self._created_at

    @property
    def data(self):
        """The data payload of the response."""
        return self.response["data"]

    @property
    def response(self):
        """The response for this tournament resource."""
        if self._response is None:
            self._response = self._pubg._core.tournament(self.id)
        return self._response

    @property
    def id(self):
        """The tournament id."""
        return self._id

    @property
    def match_ids(self):
        """The match ids associated with this tournament."""
        return [
            m["id"] for m in self.response["included"]
        ]

    def get_matches(self):
        """Get a list of match objects for the tournament matches."""
        return [
            Match(self._pubg, match_id, shard=self.shard) for match_id in self.match_ids
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
