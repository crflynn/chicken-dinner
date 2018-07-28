"""PUBG API JSON wrapper."""
import datetime
import logging
import time

import requests
from requests.exceptions import RequestException

from chicken_dinner.constants import SHARD_URL
from chicken_dinner.constants import STATUS_URL
from chicken_dinner.constants import TOURNAMENTS_URL
from chicken_dinner.constants import SHARDS
from chicken_dinner.constants import PLAYER_FILTERS


SLEEP_BUFFER = 2
MONTHNAMES = [
    None,  # placeholder index
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
UTC = datetime.timezone(datetime.timedelta(0))


class PUBGCore(object):
    """Low level interface to the PUBG JSON API.

    Provides methods for interfacing directly with the PUBG JSON API. Returns
    deserialized JSON responses.

    Info: https://documentation.playbattlegrounds.com/en/introduction.html

    :param str api_key: your PUBG api key
    :param str shard: (optional) the shard to use in all requests for this
        instance
    :param bool gzip: (optional) compress responses as gzip
    """

    def __init__(self, api_key, shard=None, gzip=True):
        self.session = requests.Session()
        self.api_key = api_key
        if gzip:
            self.session.headers.update({
                "Accept-Encoding": "gzip",
            })
        if shard is None or shard in SHARDS:
            self.shard = shard
        else:
            raise ValueError("Invalid shard provided.")
        # Set some defaults to ensure the first API call is attempted
        self._rate_limit_remaining = 10
        self._rate_limit_reset = 0

    @property
    def api_key(self):
        """The API key being used."""
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
        elif shard not in SHARDS:
            raise ValueError("Invalid shard provided.")
        else:
            return shard

    def _get(self, url, params=None, limited=True):
        if limited:
            reset_time = self._rate_limit_reset - time.time()
            if self._rate_limit_remaining == 0 and reset_time > 0:
                sleep_duration = reset_time + SLEEP_BUFFER
                logging.warning(
                    "Rate limited by PUBGCore. Sleeping for " +
                    str(int(sleep_duration)) + " seconds."
                )
                time.sleep(sleep_duration)

        response = self.session.get(url, params=params)
        logging.debug(response.headers)

        try:
            response.raise_for_status()
        except RequestException as exc:
            if response.status_code == 429:
                reset_time = self._get_rate_limit_delta(response)
                sleep_duration = int(reset_time) + SLEEP_BUFFER
                logging.warning(
                    "Rate limited by API (429). Sleeping for " +
                    str(int(sleep_duration)) + " seconds."
                )
                time.sleep(sleep_duration)
            else:
                raise exc
            # Try again and just raise on failure because something else
            # must be wrong. Hard failures should be handled by end-user
            # gracefully.
            response = self.session.get(url, params=params)
            response.raise_for_status()

        delta = self._get_rate_limit_delta(response)

        self._rate_limit_reset = time.time() + delta
        self._rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])

        return response

    def _get_rate_limit_delta(self, response):
        server_datetime = response.headers["Date"].split(" ")
        server_hms = server_datetime[4].split(":")

        server_time = datetime.datetime(
            year=int(server_datetime[3]),
            month=MONTHNAMES.index(server_datetime[2]),
            day=int(server_datetime[1]),
            hour=int(server_hms[0]),
            minute=int(server_hms[1]),
            second=int(server_hms[2]),
            tzinfo=UTC
        ).timestamp()

        reset_time = int(response.headers["X-RateLimit-Reset"])
        delta = reset_time - server_time

        return delta

    def match(self, match_id, shard=None):
        """Get a response from the match endpoint.

        Description: https://documentation.playbattlegrounds.com/en/matches-endpoint.html

        Calls here do not apply to the rate limit.

        :param str match_id: the ``match_id`` to query
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the json response from ``/{shard}/matches/{match_id}``
        """
        shard = self._check_shard(shard)
        url = SHARD_URL + shard + "/matches/" + match_id
        return self._get(url, limited=False).json()

    def player(self, player_id, shard=None):
        """Get a response from the player endpoint.

        Endpoints: https://documentation.playbattlegrounds.com/en/players-endpoint.html

        :param str player_id: the PUBG ``player_id`` (account id) to query
        :param str shard: (optional) the ``shard`` to use if different from
            the one used on instantiation
        :return: the JSON response from ``/{shard}/players/{player_id}``
        """
        shard = self._check_shard(shard)
        url = SHARD_URL + shard + "/players/" + str(player_id)
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
        shard = self._check_shard(shard)
        url = SHARD_URL + shard + "/players/" + str(player_id)
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
        shard = self._check_shard(shard)
        if filter_type not in PLAYER_FILTERS:
            raise ValueError("Filter type must be in " + str(PLAYER_FILTERS))
        if isinstance(filter_value, list):
            filter_value = ",".join(filter_value)

        params = {"filter[" + PLAYER_FILTERS[filter_type] + "]": filter_value}
        url = SHARD_URL + shard + "/players"
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
        shard = self._check_shard(shard)
        url = SHARD_URL + shard + "/samples"
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
        shard = self._check_shard(shard)
        url = SHARD_URL + shard + "/seasons"
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

    def tournament(self, tournament_id):
        """Get information about a tournament.

        Description: https://documentation.playbattlegrounds.com/en/tournaments-endpoint.html#/Tournaments/get_tournaments__id_

        :param str tournament_id: the tournament ID on which to retrieve data
        :return: the JSON response for the tournament id
        """
        return self._get(TOURNAMENTS_URL + "/" + tournament_id).json()

    def tournaments(self):
        """Get a list of tournaments.

        Description: https://documentation.playbattlegrounds.com/en/tournaments-endpoint.html#/Tournaments/get_tournaments

        :return: the JSON response for the tournaments endpoint
        """
        return self._get(TOURNAMENTS_URL).json()
