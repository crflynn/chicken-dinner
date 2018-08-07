import json

from .secret import api_key

from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG

pubg = PUBG(api_key, "pc-na")
shroud = pubg.players_from_names("badshroud")[0]

shroud_season = shroud.get_current_season()
print(shroud_season.game_mode_stats())

for match_id in shroud.match_ids:
    match = pubg.match(match_id)
    print(match.game_mode)
