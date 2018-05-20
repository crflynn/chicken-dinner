import json

from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.visual.match import create_match_animation

if __name__ == "__main__":
    # Load temp
    t = json.load(open("secret.json", "r"))
    telemetry = Telemetry.from_json(t)

    telemetry.animation(
        "match.html",
        zoom=True,
        labels=True,
        label_players=None,
        highlight_teams=["shroud"],
        size=5,
        use_hi_res=True,
        color_teams=True
    )
