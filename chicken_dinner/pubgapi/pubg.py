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
    """PUBG API Interface."""

    def __init__(self, api_key, shard=None, gzip=True):
        self._core = PUBGCore(api_key, gzip=gzip)
        self.shard = shard

    def current_season(self, shard):
        return Seasons(self, shard).current()

    def match(self, shard, match_id):
        return Match(self, shard, match_id)

    def samples(self, shard):
        return Samples(self, shard)

    def seasons(self, shard):
        return Seasons(self, shard)

    def status(self):
        return Status(self)

    def player_season(self, shard, player_id, season_id):
        if season_id == "current":
            season_id = self.current_season(shard).id
        if isinstance(player_id, Player):
            player_id = player_id.id
        return PlayerSeason(self, shard, player_id, season_id)

    def player(self, shard, player_id):
        return Player(self, shard, player_id)

    def players(self, shard, filter_type, filter_value):
        return Players(self, shard, filter_type, filter_value)

    def players_from_ids(self, shard, player_ids):
        return Players(self, shard, "player_ids", player_ids)

    def players_from_names(self, shard, player_names):
        return Players(self, shard, "player_names", player_names)

    def telemetry(self, url):
        return Telemetry(self, url)
