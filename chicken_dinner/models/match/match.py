"""Match model."""
from .asset import Asset
from .participant import Participant
from .roster import Roster
from chicken_dinner.models.constants import game_mode_to_gp
from chicken_dinner.models.constants import map_to_map_name


class Match(object):
    """Match object."""

    def __init__(self, pubg, shard, match_id):
        self._pubg = pubg
        self.shard = shard
        self.match_id = match_id
        self.response = self._pubg._core.match(shard, match_id)
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
                self.asset = Asset(pubg, shard, item)

        self.rosters = [
            Roster(pubg, shard, self, self.response["included"][idx])
            for idx in rosters_idx
        ]


    @property
    def asset_id(self):
        return self.asset.id

    @property
    def data(self):
        return self.response["data"]

    @property
    def created_at(self):
        return self.data["attributes"]["createdAt"]

    @property
    def duration(self):
        return self.data["attributes"]["duration"]

    @property
    def game_mode(self):
        return game_mode_to_gp[self.data["attributes"]["gameMode"]]

    @property
    def id(self):
        return self.data["id"]

    @property
    def map_name(self):
        return map_to_map_name[self.data["attributes"]["mapName"]]

    @property
    def participants(self):
        return [
            participant for roster in self.rosters
            for participant in roster.participants
        ]

    @property
    def stats(self):
        return self.data["attributes"]["stats"]

    @property
    def tags(self):
        return self.data["attributes"]["tags"]

    @property
    def title_id(self):
        return self.data["attributes"]["titleId"]

    @property
    def url(self):
        return self.data["links"]["self"]

    @property
    def telemetry_url(self):
        return self.asset.url

    def get_telemetry(self):
        return Telemetry(self._pubg, self.shard, self._pubg._core.get(self.asset.url))

    @property
    def rosters_player_names(self):
        return {
            roster.id: roster.player_names for roster in self.rosters
        }

    @property
    def winner(self):
        for roster in self.rosters:
            if roster.won == True:
                return roster
