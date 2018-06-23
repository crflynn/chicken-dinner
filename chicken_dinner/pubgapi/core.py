# flake8: noqa
import requests

from chicken_dinner.pubgapi.rate_limiter import DEFAULT_CALL_COUNT
from chicken_dinner.pubgapi.rate_limiter import DEFAULT_CALL_WINDOW
from chicken_dinner.pubgapi.rate_limiter import RateLimiter
from chicken_dinner.constants import BASE_URL
from chicken_dinner.constants import SHARD_URL
from chicken_dinner.constants import STATUS_URL
from chicken_dinner.constants import SHARDS
from chicken_dinner.constants import PLAYER_FILTERS


class PUBGCore(object):
    """Low level interface to the PUBG JSON API.

    Provides methods for interfacing directly with the PUBG JSON API. Returns
    deserialized JSON responses.

    Info: https://documentation.playbattlegrounds.com/en/introduction.html

    :param str api_key: your PUBG api key
    :param str shard: (optional) the shard to use in all requests for this
        instance
    :param bool gzip: (optional) compress responses as gzip
    :param int limit_call_count: (optional) your api key rate limit count
    :param int limit_call_window: (optional) your api key rate limit window
    """

    def __init__(self, api_key, shard=None, gzip=True,
                 limit_call_count=DEFAULT_CALL_COUNT,
                 limit_call_window=DEFAULT_CALL_WINDOW):
        self.session = requests.Session()
        self.api_key = api_key
        if gzip:
            self.session.headers.update({
                "Accept-Encoding": "gzip",
            })
        self.rate_limiter = RateLimiter(limit_call_count, limit_call_window)
        self.shard = shard

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        self.session.headers = {
            "Authorization": "Bearer " + value,
            "Accept": "application/vnd.api+json",
        }

    def _check_shard(self, shard):
        shard = shard or self.shard
        if shard is None:
            raise ValueError("A shard must be provided.")

    def _get(self, url, params=None, limited=True):
        if limited and self.rate_limiter.window > 0:
            self.rate_limiter.call()
        response = self.session.get(url, params=params)
        return response

    def match(self, match_id, shard=None):
        """Get a response from the match endpoint.

        Description: https://documentation.playbattlegrounds.com/en/matches-endpoint.html

        Calls here do not apply to the rate limit.

        :param str match_id: the ``match_id`` to query
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the json response from ``/{shard}/matches/{match_id}``
        """
        self._check_shard(shard)
        url = SHARD_URL + self.shard + "/matches/" + match_id
        return self._get(url, limited=False).json()

    def player(self, player_id, shard=None):
        """Get a response from the player endpoint.

        Endpoints: https://documentation.playbattlegrounds.com/en/players-endpoint.html

        :param str player_id: the PUBG ``player_id`` (account id) to query
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the JSON response from ``/{shard}/players/{player_id}``
        """
        self._check_shard(shard)
        url = SHARD_URL + self.shard + "/players/" + str(player_id)
        return self._get(url).json()

    def player_season(self, player_id, season_id, shard=None):
        """Get a response from the player/season endpoint.

        Endpoints: https://documentation.playbattlegrounds.com/en/players-endpoint.html

        :param str player_id: the PUBG ``player_id`` (account id) to query
        :param str season: the ``season_id`` to query
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the JSON response from
            ``/{shard}/players/{player_id}/seasons/{season_id}``
        """
        self._check_shard(shard)
        url = SHARD_URL + self.shard + "/players/" + str(player_id)
        url = url + "/seasons/" + str(season_id)
        return self._get(url).json()

    def players(self, filter_type, filter_value, shard=None):
        """Get a response from the players endpoint.

        Description: https://documentation.playbattlegrounds.com/en/players-endpoint.html

        :param str filter_type: query by either "player_ids" or "player_names"
        :param list filter_value: a list of strings of the ``player_ids`` or
            ``player_names`` to search
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the response from the ``/{shard}/players`` endpoint
        """
        self._check_shard(shard)
        if filter_type not in PLAYER_FILTERS:
            raise ValueError("Filter type must be in " + str(PLAYER_FILTERS))
        if isinstance(filter_value, list):
            filter_value = ",".join(filter_value)

        params = {"filter[" + PLAYER_FILTERS[filter_type] + "]": filter_value}
        url = SHARD_URL + self.shard + "/players"
        return self._get(url, params).json()

    def samples(self, start=None, shard=None):
        """Get a response from the samples endpoint.

        Description: https://documentation.playbattlegrounds.com/en/samples-endpoint.html

        :param str start: (optional) the start timestamp from which to get
            samples
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the JSON response from the ``/{shard}/samples`` endpoint
        """
        self._check_shard(shard)
        url = SHARD_URL + self.shard + "/samples"
        params = {}
        if start is not None:
            params = {"filter[createdAt-start]": start}
        return self._get(url, params).json()

    def seasons(self, shard=None):
        """Get a response from the seasons endpoint.

        Description: https://documentation.playbattlegrounds.com/en/players-endpoint.html#/Seasons/get_seasons

        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the JSON response from the ``/{shard}/seasons`` endpoint.
        """
        self._check_shard(shard)
        url = SHARD_URL + self.shard + "/seasons"
        return self._get(url).json()

    def status(self):
        """Get a response from the status endpoint.

        Description: https://documentation.playbattlegrounds.com/en/status-endpoint.html

        :return: the JSON response from the ``/status`` endpoint.
        """
        return self._get(STATUS_URL).json()

    def telemetry(self, url):
        """Download the telemetry data.

        Description: https://documentation.playbattlegrounds.com/en/telemetry.html

        Calls here do not apply to the rate limit.

        :param str url: the telemetry data URL
        :return: the JSON response for the telemetry URL
        """
        return self._get(url, limited=False).json()
