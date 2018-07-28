"""Match model."""
from .asset import Asset
from .roster import Roster
from chicken_dinner.constants import game_mode_to_gp
from chicken_dinner.constants import map_to_map_name
from chicken_dinner.models.telemetry import Telemetry


class Match(object):
    """Match object.

    :param pubg: a PUBG instance
    :param str match_id: the ``match_id`` for this match
    :param str shard: the shard for this match
    """

    def __init__(self, pubg, match_id, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The match id for this match
        self.match_id = match_id
        #: The API response for this object
        self.response = self._pubg._core.match(match_id, shard)
        self.roster_to_participant = {}
        self.participant_to_roster = {}
        self._participant_data = {}
        rosters_idx = []
        for idx, item in enumerate(self.response["included"]):
            if item["type"] == "roster":
                rosters_idx.append(idx)
                self.roster_to_participant[item["id"]] = []
                for participant in item["relationships"]["participants"]["data"]:
                    self.roster_to_participant[item["id"]].append(participant["id"])
                    self.participant_to_roster[participant["id"]] = item["id"]
            elif item["type"] == "participant":
                self._participant_data[item["id"]] = item
            elif item["type"] == "asset":
                self.asset = Asset(pubg, self, item, shard)

        #: A list of Roster instances for this match
        self.rosters = [
            Roster(pubg, self, self.response["included"][idx], shard)
            for idx in rosters_idx
        ]

    @property
    def shard(self):
        """The shard for this match."""
        return self._shard or self._pubg.shard

    @property
    def asset_id(self):
        """The asset id for this match."""
        return self.asset.id

    @property
    def data(self):
        """The data payload from the response for this match."""
        return self.response["data"]

    @property
    def created_at(self):
        """When the match was created."""
        return self.data["attributes"]["createdAt"]

    @property
    def duration(self):
        """The duration of the match."""
        return self.data["attributes"]["duration"]

    @property
    def game_mode(self):
        """The game mode for the match."""
        return game_mode_to_gp[self.data["attributes"]["gameMode"]]

    @property
    def id(self):
        """The match id."""
        return self.data["id"]

    @property
    def map_name(self):
        """The name of the map on which this match was played."""
        return map_to_map_name[self.data["attributes"]["mapName"]]

    @property
    def map_id(self):
        """The map id on which this match was played."""
        return self.data["attributes"]["mapName"]

    @property
    def participants(self):
        """A list of Participant instances for match participants."""
        return [
            participant for roster in self.rosters
            for participant in roster.participants
        ]

    @property
    def stats(self):
        """Stats for this match."""
        return self.data["attributes"]["stats"]

    @property
    def tags(self):
        """Tags associated with this match."""
        return self.data["attributes"]["tags"]

    @property
    def title_id(self):
        """The title id associated with this match."""
        return self.data["attributes"]["titleId"]

    @property
    def url(self):
        """The URL for this match resource."""
        return self.data["links"]["self"]

    @property
    def telemetry_url(self):
        """The URL for the telemetry data for this match."""
        return self.asset.url

    def get_telemetry(self, map_assets=False):
        """Download match telemetry and create a Telemetry object instance.

        :param bool map_assets: whether to map asset ids to named values, e.g.
            map ``Item_Weapon_AK47_C`` to ``AKM``.
        :return: a :class:`chicken_dinner.models.telemetry.Telemetry` instance
            for this match.
        """
        return Telemetry(self._pubg, self.telemetry_url, shard=self.shard)

    @property
    def rosters_player_names(self):
        """A mapping of roster_ids to player names for this match."""
        return {
            roster.id: roster.player_names for roster in self.rosters
        }

    @property
    def winner(self):
        """The Roster instance for the winner of this match."""
        for roster in self.rosters:
            if roster.won:
                return roster

    @property
    def is_custom(self):
        """Whether or not the match is a custom match."""
        return self.data["attributes"]["isCustomMatch"]
