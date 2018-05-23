"""Match participant model."""
from chicken_dinner.util import camel_to_snake


class Participant(object):
    """Participant model.

    :param pubg: a PUBG instance
    :param match: the match object associated with this participant
    :param roster: the roster object associated with this participant
    :param data: the data payload from the participant response object
    :param str shard: the shard for the match for this participant
    """

    def __init__(self, pubg, match, roster, data, shard=None):
        self._pubg = pubg
        self._shard = shard
        #: The Match instance associated with this participant
        self.match = match
        #: The Roster instance associated with this participant
        self.roster = roster
        #: The data payload associated with this participant
        self.data = data
        #: Stats associated with this participant
        self.stats = {
            camel_to_snake(k): v
            for k, v in self.data["attributes"]["stats"].items()
        }

    @property
    def shard(self):
        """The shard for the match associated with this participant."""
        return self._shard or self._pubg.shard

    @property
    def id(self):
        """The player's account id."""
        return self.data["id"]

    @property
    def participant_id(self):
        """The match specific participant id of the player."""
        return self.data["id"]

    @property
    def player_id(self):
        """The player's account id."""
        return self.data["attributes"]["stats"]["playerId"]

    @property
    def name(self):
        """The player's in-game name."""
        return self.data["attributes"]["stats"]["name"]

    @property
    def actor(self):
        return self.data["attributes"]["actor"]

    @property
    def teammates(self):
        """A list of participant objects for this player's teammates."""
        return [
            p for p in self.roster.participants
            if p.participant_id != self.participant_id
        ]

    @property
    def teammates_player_names(self):
        """A list of player names for this player's teammates."""
        return [p.name for p in self.teammates]

    @property
    def teammates_player_ids(self):
        """A list of player account ids for this player's teammates."""
        return [p.player_id for p in self.teammates]

    @property
    def won(self):
        """Whether or not this player's team won the associated match."""
        return self.roster.won

    def get_player(self):
        """Get a Player object for this participant."""
        return self._pubg.player(self.player_id, self.shard)

    def get_player_season(self, season_id):
        """Get a PlayerSeason object for this participant.

        :param str season_id: the season id for which to retreive data
        """
        return self._pubg.player_season(self.player_id, season_id, self.shard)

    def get_current_player_season(self):
        """Get a PlayerSeason object for the current season."""
        return self.get_player_season("current")
