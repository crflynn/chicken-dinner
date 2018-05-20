"""Telemetry class."""
import datetime

from chicken_dinner.structures import CaseInsensitiveDict


class Telemetry(object):

    def __init__(self, pubg, shard, url, telemetry_json=None):
        self._pubg = pubg
        if telemetry_json is not None:
            self.response = telemetry_json
        else:
            self.response = self._pubg._core.telemetry(url)
        self.telemetry = CaseInsensitiveDict.from_json(self.response)
        self.shard = shard
        if "common" in self.telemetry[-1]:
            self.platform = "pc"
        else:
            self.platform = "xbox"
        self.is_pc = "pc" == self.platform
        self.is_xbox = "xbox" == self.platform

    # @property
    # def response():
    #     return [element.to_json() for element in self.telemetry]

    def filter_by(self, event_type=None): #, account_id=None, player_name=None):
        events = None
        if event_type is not None:
            event_type = event_type.lower().replace("_", "")
            if not event_type.startswith("log"):
                event_type = "log" + event_type
            events = [
                event for event in self.telemetry
                if event["_T"].lower() == event_type
            ]
        else:
            events = [event for event in self.telemetry]

        return events

    def accounts(self):
        accounts = []
        for event in self.telemetry:
            if event["_T"].lower() == "logplayerlogin":
                accounts.append(event["accountId"])
        return accounts

    def players(self):
        players = {}
        for event in self.telemetry:
            if event["_T"].lower() == "logplayercreate":
                players[event["character"]["name"]] = event["character"]["accountId"]
        return players

    def player_names(self):
        player_names = []
        for event in self.telemetry:
            if event["_T"].lower() == "logplayercreate":
                player_names.append(event["character"]["name"])
        return player_names

    def damage_done(player=None, combat_only=True, distribution=False):
        damage = {}
        for event in self.telemetry:
            if event["_T"].lower() == "logplayertakedamage":
                attacker = event["attacker"]["name"]
                if player is not None and player != attacker:
                    continue
                if attacker == "":
                    if combat_only:
                        continue
                    else:
                        attacker = "[" + event["damageTypeCategory"] + "]"
                if distribution:
                    if attacker not in damage:
                        damage[attacker] = {}
                    if victim not in damage[attacker]:
                        damage[attacker][victim] = event["damage"]
                    else:
                        damage[attacker][victim] += event["damage"]
                else:
                    if attacker not in damage:
                        damage[attacker] = event["damage"]
                    else:
                        damage[attacker] += event["damage"]
        return damage

    def damage_taken(player=None, combat_only=True, distribution=False):
        damage = {}
        for event in self.telemetry:
            if event["_T"].lower() == "logplayertakedamage":
                victim = event["victim"]["name"]
                if player is not None and player != victim:
                    continue
                attacker = event["attacker"]["name"]
                if attacker == "":
                    if combat_only:
                        continue
                    else:
                        attacker = "[" + event["damageTypeCategory"] + "]"
                if distribution:
                    if victim not in damage:
                        damage[victim] = {}
                    if attacker not in damage[attacker]:
                        damage[victim][attacker] = event["damage"]
                    else:
                        damage[victim][attacker] += event["damage"]
                else:
                    if victim not in damage:
                        damage[victim] = event["damage"]
                    else:
                        damage[victim] += event["damage"]
        return damage

    def rosters(self):
        rosters = {}
        for event in self.telemetry[::-1]:
            if event["_T"] == "LogMatchEnd":
                for player in event["characters"]:
                    team = player["teamId"]
                    player_name = player["name"]
                    if team not in rosters:
                        rosters[team] = []
                    rosters[team].append(player_name)
        return rosters

    def num_players(self):
        return len(self.player_names())

    def num_teams(self):
        return len(self.rosters())

    def rankings(rank=None):
        rankings = {}
        for event in self.telemetry[::-1]:
            if event["_T"] == "LogMatchEnd":
                for player in event["characters"]:
                    ranking = player["ranking"]
                    if ranking not in rankings:
                        rankings[ranking] = []
                    rankings[ranking].append(player["name"])
        if rank is not None:
            return rankings.get(rank, None)
        return rankings

    def winner(self):
        return self.rankings(rank=1)

    @classmethod
    def from_json(cls, telemetry_json, pubg=None, shard=None, url=None):
        return cls(pubg, shard, url, telemetry_json)

    def map_name(self):
        common = self.telemetry[-1].get("common", None)
        if common is not None:
            return common["mapName"]
        else:
            return None

    def match_id(self):
        common = self.telemetry[-1].get("common", None)
        if common is not None:
            return common["matchId"]
        else:
            return None

    def player_positions(self, include_pregame=False):
        locations = self.filter_by("logplayerposition")
        if not include_pregame:
            locations = [
                location for location in locations
                if location["elapsedTime"] > 0
            ]
        player_positions = {}
        start = datetime.datetime.strptime(
            locations[0]["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        for location in locations:
            player = location["character"]["name"]
            if player not in player_positions:
                player_positions[player] = []
            # (t, x, y, z)
            timestamp = datetime.datetime.strptime(
                location["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            dt = (timestamp - start).total_seconds()
            player_positions[player].append(
                (
                    dt,
                    location["character"]["location"]["x"],
                    location["character"]["location"]["y"],
                    location["character"]["location"]["z"],
                )
            )

        return player_positions

    def circle_positions(self):
        game_states = self.filter_by("loggamestateperiodic")
        circle_positions = {
            "white": [],
            "blue": [],
            "red": [],
        }
        start = datetime.datetime.strptime(
            game_states[0]["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        for game_state in game_states:
            timestamp = datetime.datetime.strptime(
                game_state["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            dt = (timestamp - start).total_seconds()
            circle_positions["blue"].append(
                (
                    dt,
                    game_state["gameState"]["safetyZonePosition"]["x"],
                    game_state["gameState"]["safetyZonePosition"]["y"],
                    game_state["gameState"]["safetyZonePosition"]["z"],
                    game_state["gameState"]["safetyZoneRadius"],
                )
            )
            circle_positions["red"].append(
                (
                    dt,
                    game_state["gameState"]["redZonePosition"]["x"],
                    game_state["gameState"]["redZonePosition"]["y"],
                    game_state["gameState"]["redZonePosition"]["z"],
                    game_state["gameState"]["redZoneRadius"],
                )
            )
            circle_positions["white"].append(
                (
                    dt,
                    game_state["gameState"]["poisonGasWarningPosition"]["x"],
                    game_state["gameState"]["poisonGasWarningPosition"]["y"],
                    game_state["gameState"]["poisonGasWarningPosition"]["z"],
                    game_state["gameState"]["poisonGasWarningRadius"],
                )
            )
        return circle_positions

    def match_length(self):
        for event in self.telemetry[::-1]:
            elapsed_time = event.get("elapsedTime", None)
            if elapsed_time is not None:
                return elapsed_time
