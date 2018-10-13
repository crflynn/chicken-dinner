import logging

from chicken_dinner.pubgapi import PUBG
from .secret import api_key
from .secret import shard
from .secret import match_id
# from tests.secret import api_key


logger = logging.getLogger()
logger.setLevel("INFO")


if __name__ == "__main__":
    # api_key = "your_api_key"
    # pubg = PUBG(api_key, "xbox-na")
    pubg = PUBG(api_key, shard)
    match = pubg.match(match_id)
    telemetry = match.get_telemetry()

    telemetry.playback_animation(
        "secret_test.html",
        zoom=True,
        labels=True,
        label_players=[],
        # highlight_teams=["shroud"],
        highlight_winner=True,
        label_highlights=True,
        size=6,
        end_frames=60,
        use_hi_res=False,
        color_teams=True,
        interpolate=True,
        damage=True,
        interval=2,
        fps=30,
    )
