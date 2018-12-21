import logging

from chicken_dinner.pubgapi import PUBG
from .secret import api_key
# from tests.secret import api_key


logger = logging.getLogger()
logger.setLevel("INFO")


if __name__ == "__main__":
    # api_key = "your_api_key"
    # pubg = PUBG(api_key, "xbox-na")
    pubg = PUBG(api_key, "steam")
    player = "chocoTaco"
    shroud = pubg.players_from_names(player)[0]
    print(shroud)
    print(shroud.match_ids)
    for match_id in shroud.match_ids:
        match = pubg.match(match_id)
        print(match.map_name)
        if match.map_name not in ("DihorOtok_Main", "Vikendi"):
            print(match.map_name, match_id)
            match_telemetry = match.get_telemetry()
            # break
            match_telemetry.playback_animation(
                "secret.html",
                zoom=True,
                labels=True,
                label_players=[],
                # highlight_teams=["shroud"],
                highlight_winner=True,
                label_highlights=True,
                size=6,
                end_frames=60,
                use_hi_res=False,
                use_no_text=True,
                color_teams=True,
                interpolate=True,
                damage=True,
                interval=2,
                fps=30,
            )
            print(match.map_name, match_id)
            break
