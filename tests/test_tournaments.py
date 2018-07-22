import json

from .secret import api_key

from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG

# core = PUBGCore(api_key)
# tournaments = core.tournaments()
# print(json.dumps(tournaments, indent=2))
# tid = tournaments["data"][0]["id"]
# tournament = core.tournament(tid)
# print(json.dumps(tournament, indent=2))

pubg = PUBG(api_key, "pc-tournament")
tournaments = pubg.tournaments()
print(tournaments.response)
tournament = tournaments[0]
print(tournament.response)
tournament.created_at
tournament.data
tournament.id
tournament.response
tournament.match_ids
tournament.meta
tournament.url
matches = tournament.get_matches()
