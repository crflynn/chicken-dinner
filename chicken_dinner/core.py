# flake8: noqa
import requests

from .rate_limiter import DEFAULT_CALL_COUNT
from .rate_limiter import DEFAULT_CALL_WINDOW
from .rate_limiter import RateLimiter


BASE_URL = "https://api.playbattlegrounds.com"
SHARD_URL = BASE_URL + "/shards/"
STATUS_URL = BASE_URL + "/status"
PLAYER_FILTERS = {
    "player_ids": "playerIds",
    "player_names": "playerNames",
}
SHARDS = [
    "xbox-as",
    "xbox-eu",
    "xbox-na",
    "xbox-oc",
    "pc-krjp",
    "pc-jp",
    "pc-na",
    "pc-eu",
    "pc-oc",
    "pc-kakao",
    "pc-sea",
    "pc-sa",
    "pc-as",
]


class PUBGCore(object):

    def __init__(self, api_key, gzip=True,
                 limit_call_count=DEFAULT_CALL_COUNT,
                 limit_call_window=DEFAULT_CALL_WINDOW):
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": "Bearer " + api_key,
            "Accept": "application/vnd.api+json",
        }
        if gzip:
            self.session.headers.update({
                "Accept-Encoding": "gzip",
            })
        self.rate_limiter = RateLimiter(limit_call_count, limit_call_window)

    def _get(self, url, params=None):
        if self.rate_limiter.window > 0:
            self.rate_limiter.call()
        response = self.session.get(url, params=params)
        return response

    def match(self, shard, match_id):
        url = SHARD_URL + shard + "/matches/" + match_id
        return self._get(url).json()

    def player(self, shard, player_id, season_id=None):
        url = SHARD_URL + shard + "/players/" + str(player_id)
        if season_id is not None:
            url = url + "/seasons/" + str(season_id)
        return self._get(url).json()

    def players(self, shard, filter_type, filter_value):
        if filter_type not in PLAYER_FILTERS:
            raise ValueError("Filter type must be in " + str(PLAYER_FILTERS))
        if isinstance(filter_value, list):
            filter_value = ",".join(filter_value)

        params = {"filter[" + PLAYER_FILTERS[filter_type] + "]": filter_value}
        url = SHARD_URL + shard + "/players"
        return self._get(url, params).json()

    def samples(self, shard, start=None):
        url = SHARD_URL + shard + "/samples"
        params = {}
        if start is not None:
            params = {"filter[createdAt-start]": start}
        return self._get(url, params).json()

    def seasons(self, shard):
        url = SHARD_URL + shard + "/seasons"
        return self._get(url).json()

    def status(self):
        return self._get(STATUS_URL).json()

    def telemetry(self, url):
        return self._get(url).json()
