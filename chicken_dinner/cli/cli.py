import os

import click

from chicken_dinner.pubgapi import PUBG
from chicken_dinner.assets.maps import update_maps
from chicken_dinner.assets.dictionary import update_dictionary


@click.group()
def cli():
    pass


@click.command()
def assets():
    click.echo(click.style("Updating maps", fg="yellow"))
    update_maps()
    click.echo(click.style("Updating asset dictionary", fg="yellow"))
    update_dictionary()


@click.command()
def leaderboard():
    pass


@click.command()
def stats():
    pass


@click.command()
@click.option("--api-key", default=os.environ["PUBG_API_KEY"], help="pubg api key")
@click.option("--shard", default="steam", help="pubg api shard")
@click.option("-w", "--wins-only", is_flag=True, help="wins only")
@click.option("-l", "--latest", is_flag=True, help="latest match")
@click.option("-s", "--size", default=6, help="render size")
# TODO path
@click.argument("player_name")
def replay(api_key, shard, wins_only, latest, size, player_name):
    pubg = PUBG(api_key, shard)
    player = pubg.players_from_names(player_name)[0]
    for match_id in player.match_ids:
        match = pubg.match(match_id)
        click.echo("Match ID: " + match_id)
        if wins_only and player_name not in match.winner.player_names:
            continue
        else:
            click.echo(click.style("Downloading: " + match_id, fg="yellow"))
            match_telemetry = match.get_telemetry()
            click.echo(click.style("Rendering: " + match_id, fg="yellow"))
            filename = player_name + "_" + match.created_at.replace("-", "").replace(":", "") + "_" + match_id + ".html"
            match_telemetry.playback_animation(
                filename,
                zoom=True,
                labels=True,
                label_players=[player_name],
                highlight_winner=True,
                label_highlights=True,
                size=size,
                end_frames=60,
                use_hi_res=False,
                color_teams=False if "solo" in match.game_mode else True,
                interpolate=True,
                damage=True,
                interval=2,
                fps=30,
            )
            click.echo(click.style("Saved: " + filename, fg="green"))
            if latest:
                break


cli.add_command(replay, name="replay")
cli.add_command(assets, name="assets")
cli.add_command(leaderboard, name="leaderboard")
cli.add_command(stats, name="stats")
