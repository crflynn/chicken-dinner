# flake8: noqa
from chicken_dinner.pubgapi.core import PUBGCore
from chicken_dinner.models.match import Match
from chicken_dinner.models import Player
from chicken_dinner.models import Players
from chicken_dinner.models import PlayerSeason
from chicken_dinner.models import Samples
from chicken_dinner.models import Seasons
from chicken_dinner.models import Status


class PUBG(object):
    """High level type-based interface to the PUBG JSON API.

    :param str api_key: your PUBG api key
    :param str shard: (optional) a shard to use for all requests with this
        instance
    :param bool gzip: (default=*True*) whether to gzip the responses. Responses
        are automatically unzipped by the underlying ``requests`` library.
    """

    def __init__(self, api_key, shard=None, gzip=True):
        self._core = PUBGCore(api_key, gzip=gzip)
        self.shard = shard

    def set_api_key(self, api_key):
        """Set the PUBG api key.

        :param str api_key: your PUBG api key.
        """
        self._core.api_key = api_key

    def set_shard(self, shard):
        """Set the shard.

        :param str shard: the shard to use for requests with this instance
        """
        self.shard = shard

    def _check_shard(self, shard):
        shard = shard or self.shard
        if shard is None:
            raise ValueError("A shard must be provided.")

    def current_season(self, shard=None):
        """Get the current season.

        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: a :class:`chicken_dinner.models.Season` object for the current
            season
        """
        self._check_shard(shard)
        return Seasons(self, shard).current()

    def match(self, match_id, shard=None):
        """Get match info by ``match_id``.

        :param str match_id: the match_id to query
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: a :class:`chicken_dinner.models.Match` object for the match
            corresponding to ``match_id``.
        """
        self._check_shard(shard)
        return Match(self, shard, match_id)

    def samples(self, shard=None):
        """Get match samples.

        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: a :class:`chicken_dinner.models.Samples` object containing
            match samples.
        """
        self._check_shard(shard)
        return Samples(self, shard)

    def seasons(self, shard=None):
        """Get an iterable of PUBG seasons.

        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: an iterable :class:`chicken_dinner.models.Seasons` object
            containing multiple :class:`chicken_dinner.models.Season` objects.
        """
        self._check_shard(shard)
        return Seasons(self, shard)

    def status(self):
        """Get the status of the PUBG API.

        :return: a :class:`chicken_dinner.models.Status` object containing
            information about the status of the API.
        """
        return Status(self)

    def player_season(self, player_id, season_id, shard=None):
        """Get a player's information for a particular season.

        :param str player_id: the player's account id
        :param str season_id: the PUBG season id
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: a :class:`chicken_dinner.models.PlayerSeason` object
            containing information about matches and statistics for a player's
            performance in the season given by ``season_id``
        """
        self._check_shard(shard)
        if season_id == "current":
            season_id = self.current_season(shard).id
        if isinstance(player_id, Player):
            player_id = player_id.id
        return PlayerSeason(self, shard, player_id, season_id)

    def player(self, player_id, shard=None):
        """Get a player's metadata.

        :param str player_id: the player's account id
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: a :class:`chicken_dinner.models.Player` object
            containing information about the player
        """
        self._check_shard(shard)
        return Player(self, shard, player_id)

    def players(self, filter_type, filter_value, shard=None):
        """Get multiple players' metadata.

        :param str filter_type: query by either "player_ids" or "player_names"
        :param list filter_value: a list of strings of the ``player_ids`` or
            ``player_names`` to search
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: an iterable :class:`chicken_dinner.models.Players` object
            consisting of multiple :class:`chicken_dinner.models.Player`
            objects
        """
        self._check_shard(shard)
        return Players(self, shard, filter_type, filter_value)

    def players_from_ids(self, player_ids, shard=None):
        """Get multiple players' metadata from a list of ``player_ids``.

        :param list player_ids: a list of strings of ``player_ids``
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: an iterable :class:`chicken_dinner.models.Players` object
            consisting of multiple :class:`chicken_dinner.models.Player`
            objects
        """
        self._check_shard(shard)
        return Players(self, shard, "player_ids", player_ids)

    def players_from_names(self, player_names, shard=None):
        """Get multiple players' metadata from a list of ``player_names``.

        :param list player_names: a list of strings of ``player_names``
        :param str shard: (optional) the shard to use if different from the
            instance shard
        :return: an iterable :class:`chicken_dinner.models.Players` object
            consisting of multiple :class:`chicken_dinner.models.Player`
            objects
        """
        self._check_shard(shard)
        return Players(self, shard, "player_names", player_names)

    def telemetry(self, url):
        return Telemetry(self, url)
