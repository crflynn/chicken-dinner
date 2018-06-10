import json
import logging

from chicken_dinner.models.telemetry import Telemetry

logger = logging.getLogger()
logger.setLevel("INFO")

if __name__ == "__main__":
    # Load temp
    t = json.load(open("secret.json", "r"))
    telemetry = Telemetry.from_json(t)

    telemetry.playback_animation(
        "docs/match.html",
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
        interval=2,
        fps=30,
    )
