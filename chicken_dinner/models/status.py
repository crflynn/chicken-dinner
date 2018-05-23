"""Status model."""
from chicken_dinner.constants import STATUS_URL


class Status(object):
    """Status model.

    Contains information about the status of the PUBG API.

    :param pubg: an instance of the :class:`chicken_dinner.pubgapi.PUBG` class
    """

    def __init__(self, pubg):
        self._pubg = pubg
        #: The API response for this object
        self.response = self._pubg._core.status()

    @property
    def data(self):
        """The status data payload."""
        return self.response["data"]

    @property
    def id(self):
        """Get the id of the status."""
        return self.data["id"]

    @property
    def version(self):
        """Get the API version."""
        return self.data["attributes"]["version"]

    @property
    def released_at(self):
        """Get the timestamp this version was released."""
        return self.data["attributes"]["releasedAt"]

    @property
    def url(self):
        """The status endpoint URL."""
        return STATUS_URL

    def refresh(self):
        """Refresh the api status."""
        self.response = self._pubg._core.status()
