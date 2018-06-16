"""Telemetry class."""
import datetime

from chicken_dinner.structures import CaseInsensitiveDict


class Telemetry(object):
    """Telemetry model.

    :param pubg: a PUBG instance
    :param str shard: the shard for the match associated with this telemetry
    :param str url: the url for this telemetry
    :param list telemetry_json: (optional) the raw telemetry response
    """

    def __init__(self, pubg, url, telemetry_json=None, shard=None):
        self._pubg = pubg
        self._shard = shard
        if telemetry_json is not None:
            #: The API response associated with this object
            self.response = telemetry_json
        else:
            self.response = self._pubg._core.telemetry(url)
        #: Case insensitive JSON representation of the telemetry response
        self.telemetry = CaseInsensitiveDict.from_json(self.response)
        if "common" in self.telemetry[-1]:
            #: The platform for this game, "pc" or "xbox"
            self.platform = "pc"
        else:
            self.platform = "xbox"
        #: Whether this game was played on PC
        self.is_pc = "pc" == self.platform
        #: Whether this game was played on xbox
        self.is_xbox = "xbox" == self.platform

    @property
    def shard(self):
        """The shard for this match."""
        return self._shard or self._pubg.shard

    def filter_by(self, event_type=None): #, account_id=None, player_name=None):
        """Get a list of telemetry events for a specific event type.

        :param event_type: the event type to filter
        """
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

    def player_ids(self):
        """The account ids of all players in the match."""
        accounts = []
        for event in self.telemetry:
            if event["_T"].lower() == "logplayerlogin":
                accounts.append(event["accountId"])
        return accounts

    def players(self):
        """A map of player names to account ids for all players this match."""
        players = {}
        for event in self.telemetry:
            if event["_T"].lower() == "logplayercreate":
                players[event["character"]["name"]] = event["character"]["accountId"]
        return players

    def player_names(self):
        """A list of player names for all match pariticipants."""
        player_names = []
        for event in self.telemetry:
            if event["_T"].lower() == "logplayercreate":
                player_names.append(event["character"]["name"])
        return player_names

    def damage_done(player=None, combat_only=True, distribution=False):
        """Damage done by each player in the match.

        :param str player: a player name to filter on
        :param bool combat_only: return only PvP damage (default True)
        :param bool distribution: return a player to player distribution of
            damage for the match if true. if false return total damage done
            by each player. (default False)
        """
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
        """Damage taken by each player in the match.

        :param str player: a player name to filter on
        :param bool combat_only: return only PvP damage (default True)
        :param bool distribution: return a player to player distribution of
            damage for the match if true. if false return total damage taken
            by each player. (default False)
        """
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
        """The team rosters for the match."""
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
        """Number of participants in this match."""
        return len(self.player_names())

    def num_teams(self):
        """Number of teams (rosters) in this match."""
        return len(self.rosters())

    def rankings(self, rank=None):
        """The rankings of each team from this match.

        Returns a map of rank : [players] for each team in the match.

        :param int rank: Get the specific rank number players for the match.
        """
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
        """The winner(s) of the match.

        Match winners as a list of player names.
        """
        return self.rankings(rank=1)

    @classmethod
    def from_json(cls, telemetry_json, pubg=None, url=None, shard=None):
        """Construct an instance of telemetry from the json response."""
        return cls(pubg, url, telemetry_json, shard)

    @classmethod
    def from_match_id(cls, match_id, pubg, shard=None):
        """Construct an instance of telemetry from a match id."""
        match = pubg.match(match_id, shard)
        url = match.telemetry_url()
        return cls(pubg, url, shard=shard)

    def map_name(self):
        """Get the map name for PC matches. None if not PC."""
        common = self.telemetry[-1].get("common", None)
        if common is not None:
            return common["mapName"]
        else:
            return None

    def match_id(self):
        """The match id for the match."""
        common = self.telemetry[-1].get("common", None)
        if common is not None:
            return common["matchId"]
        else:
            return None

    def player_damages(self, include_pregame=False):
        """Get the player damages for the match.

        Returns a dict of attacker players as keys and values of damage
        attacker and victim positions with the values tuples. Each tuple has
        seven elements being (t, x_a, y_a, z_a, x_v, y_v, y_z) coordinates
        where a is attacker and v is victim.

        :param bool include_pregame: (default False) whether to include
            pre-game damage positions.
        """
        start = datetime.datetime.strptime(
            self.filter_by("logmatchstart")[0]["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        damages = {}
        attack_events = self.filter_by("logplayerattack")
        attackers = {}
        for event in attack_events:
            attackers[event["attackId"]] = event["attacker"]

        damage_events = self.filter_by("logplayertakedamage")
        for event in damage_events:
            attacker = event["attacker"]["name"]
            if attacker != "":
                timestamp = datetime.datetime.strptime(
                    event["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                dt = (timestamp - start).total_seconds()
                if (not include_pregame and dt < 0) or event["attackId"] == -1:
                    continue
                if attacker not in damages:
                    damages[attacker] = []
                attacker_location = attackers[event["attackId"]]["location"]
                damages[attacker].append(
                    (
                        dt,
                        attacker_location["x"],
                        attacker_location["y"],
                        attacker_location["z"],
                        event["victim"]["location"]["x"],
                        event["victim"]["location"]["y"],
                        event["victim"]["location"]["z"],
                    )
                )
        return damages


    def player_positions(self, include_pregame=False):
        """Get the player positions for the match.

        Returns a dict of players positions up to death with keys being player
        names and values being a list of tuples. Each tuple has four elements
        being (t, x, y, z) coordinates where t is taken from the event
        timestamps.

        :param bool include_pregame: (default False) whether to include
            pre-game player positions.
        """
        start = datetime.datetime.strptime(
            self.filter_by("logmatchstart")[0]["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        locations = self.filter_by("logplayerposition")
        if not include_pregame:
            locations = [
                location for location in locations
                if location["elapsedTime"] > 0
            ]
        player_positions = {}
        dead = []
        for location in locations:
            timestamp = datetime.datetime.strptime(
                location["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            dt = (timestamp - start).total_seconds()
            player = location["character"]["name"]
            if player not in player_positions:
                player_positions[player] = []
            elif player in dead:
                continue
            # (t, x, y, z)
            player_positions[player].append(
                (
                    dt,
                    location["character"]["location"]["x"],
                    location["character"]["location"]["y"],
                    location["character"]["location"]["z"],
                )
            )
            if location["character"]["ranking"] > 1:
                dead.append(player)
        # cleanup
        for player, positions in player_positions.items():
            count = 0
            last = positions[-1]
            for pos in positions[::-1]:
                if pos == last:
                    count += 1
                else:
                    break
            player_positions[player] = positions[:-count]

        return player_positions

    def circle_positions(self):
        """Get the circle positions for the match.

        Returns a dict of circle positions with keys being circle colors and
        values being a list of tuples. Each tuple has five elements being
        (t, x, y, z, r) coordinates where t is taken from the "elapsedTime"
        field in the JSON response and r is the circle radius.

        The circle colors are "white", "blue", and "red"
        """
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

    def care_package_positions(self, land=True):
        """Get the crate positions for the match.

        Returns the crate positions for a match as a list of tuples.
        Each tuple has four elements being
        (t, x, y, z) coordinates where t is taken from the "elapsedTime"
        field in the JSON response.
        """
        start = datetime.datetime.strptime(
            self.filter_by("logmatchstart")[0]["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        if land:
            care_package_spawns = self.filter_by("logcarepackageland")
        else:
            care_package_spawns = self.filter_by("logcarepackagespawn")

        care_package_positions = []
        for care_package in care_package_spawns:
            package_time = datetime.datetime.strptime(
                care_package["_D"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            time_elapsed = (package_time - start).total_seconds()
            care_package_positions.append(
                (
                    time_elapsed,
                    care_package["itemPackage"]["location"]["x"],
                    care_package["itemPackage"]["location"]["y"],
                    care_package["itemPackage"]["location"]["z"],
                )
            )
        return care_package_positions

    def match_length(self):
        """The length of the match in seconds."""
        for event in self.telemetry[::-1]:
            elapsed_time = event.get("elapsedTime", None)
            if elapsed_time is not None:
                return elapsed_time

    def started(self):
        """A timestamp of when the match started."""
        return self.telemetry[0]["_D"]

    def killed(self):
        """A list of player names of all killed players this match."""
        deaths = self.filter_by("logplayerkill")
        players_killed = []
        for death in deaths:
            players_killed.append(death["victim"]["name"])
        return players_killed

    def playback_animation(self, filename="playback.html", **kwargs):
        """Generate a playback animation from the telemetry data.

        Generate an HTML5 animation using matplotlib and ffmpeg.
        Requires installation via ``pip install chicken-dinner[visual]``.

        :param filename: a file to generate for the animation (default
            "playback.html")
        :param bool labels: whether to label players by name
        :param int disable_labels_after: if passed, turns off player labels after
            number of seconds elapsed in game
        :param list label_players: a list of strings of player names that should
            be labeled
        :param bool dead_players: whether to mark dead players
        :param list dead_player_labels: a list of strings of players that should
            be labeled when dead
        :param bool zoom: whether to zoom with the circles through the playback
        :param float zoom_edge_buffer: how much to buffer the blue circle edge
            when zooming
        :param bool use_hi_res: whether to use the hi-res image, best to be set
            to True when using zoom
        :param bool color_teams: whether to color code different teams
        :param list highlight_teams: a list of strings of player names whose teams
            should be highlighted
        :param list highlight_players: a list of strings of player names who
            should be highlighted
        :param str highlight_color: a color to use for highlights
        :param bool highlight_winner: whether to highlight the winner(s)
        :param bool label_highlights: whether to label the highlights
        :param bool care_packages: whether to show care packages
        :param bool damage: whether to show PvP damage
        :param int end_frames: the number of extra end frames after game has been
            completed
        :param int size: the size of the resulting animation frame
        :param int dpi: the dpi to use when processing the animation
        :param bool interpolate: use linear interpolation to get frames with
            second-interval granularity
        :param int interval: interval between gameplay frames in seconds
        :param int fps: the frames per second for the animation
        """
        from chicken_dinner.visual.playback import create_playback_animation

        return create_playback_animation(self, filename, **kwargs)
