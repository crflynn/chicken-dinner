import logging

from chicken_dinner.pubgapi import PUBG


logger = logging.getLogger()
logger.setLevel("INFO")


if __name__ == "__main__":
    api_key = "your_api_key"
    pubg = PUBG(api_key, "pc-na")
    shroud = pubg.players_from_names("shroud")[0]
    for match_id in shroud.match_ids:
        match = pubg.match(match_id)
        if "shroud" in match.winner.player_names and match.map_name in ("Desert_Main", "Miramar"):
            print(match.map_name, match_id)
            match_telemetry = match.get_telemetry()
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
                color_teams=False,
                interpolate=True,
                damage=True,
                interval=2,
                fps=30,
            )
            break
