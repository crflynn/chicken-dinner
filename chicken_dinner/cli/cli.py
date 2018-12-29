"""CLI functionality.

Entry point: $ chicken-dinner [CMD] [OPTS] [player_name]
"""
from collections import defaultdict
import json
import logging
import os

import click
from tabulate import tabulate

from chicken_dinner.pubgapi import PUBG
from chicken_dinner.assets.maps import update_maps
from chicken_dinner.assets.dictionary import update_dictionary


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_pubg(api_key, shard):
    if api_key is None:
        raise ValueError("Must provide API key or environment variable 'PUBG_API_KEY'.")
    pubg = PUBG(api_key, shard)
    return pubg


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command(short_help="Update local assets")
def assets():
    """Download maps and update local asset mapping.

    usage: $ chicken-dinner assets
    """
    click.echo(click.style("Updating maps", fg="yellow"))
    update_maps()
    click.echo(click.style("Updating asset dictionary", fg="yellow"))
    update_dictionary()


@click.command(short_help="Display leaderboards")
@click.option("--api-key", default=os.environ.get("PUBG_API_KEY", None), help="pubg api key")
@click.option("--shard", default="steam", help="pubg api shard")
@click.argument("game_mode")
def leaderboard(api_key, shard, game_mode):
    """Retrieve the latest leaderboard standings.

    usage: $ chicken-dinner leaderboards --api-key=$PUBG_API_KEY --shard=steam solo-fpp
    """
    pubg = get_pubg(api_key, shard)
    leaderboards = pubg.leaderboard(game_mode=game_mode)
    click.echo(json.dumps(leaderboards.data))
    # TODO endpoint still looks broken


@click.command(short_help="Display player stats")
@click.option("--api-key", default=os.environ.get("PUBG_API_KEY", None), help="pubg api key")
@click.option("--shard", default="steam", help="pubg api shard")
@click.option("-l", "--lifetime", is_flag=True, help="lifetime stats")
@click.option("-g", "--group", default=None, help="game mode group")
@click.option("-p", "--perspective", default=None, help="game mode perspective")
@click.argument("player_name")
def stats(api_key, shard, lifetime, group, perspective, player_name):
    """Retrieve stats for a player.

    usage: $ chicken-dinner stats --api-key=$PUBG_API_KEY --shard=steam --lifetime --group=solo --perspective=fpp
    usage: $ chicken-dinner stats --api-key=$PUBG_API_KEY --shard=steam -l -g solo -p fpp
    """
    pubg = get_pubg(api_key, shard)
    player = pubg.players_from_names(player_name)[0]
    if lifetime:
        player_season = pubg.lifetime(player_id=player.id)
    else:
        player_season = player.get_current_season()
    player_season_stats = player_season.game_mode_stats(group=group, perspective=perspective)
    game_modes_stats = defaultdict(list)
    for game_mode, game_mode_stats in player_season_stats.items():
        for stat, value in game_mode_stats.items():
            if len(game_modes_stats["Stats"]) < len(game_mode_stats.keys()):
                game_modes_stats["Stats"].append(stat)
            game_modes_stats[game_mode].append(value)
    click.echo()
    click.echo(tabulate(game_modes_stats, headers="keys"))


@click.command(short_help="Generate replay visualizations")
@click.option("--api-key", default=os.environ.get("PUBG_API_KEY", None), help="pubg api key")
@click.option("--shard", default="steam", help="pubg api shard")
@click.option("-w", "--wins-only", is_flag=True, help="wins only")
@click.option("-l", "--latest", is_flag=True, help="latest match only")
@click.option("-s", "--size", default=6, help="render size")
@click.option("-p", "--path", default=".", help="the path for new files")
@click.option("-v", "--verbose", is_flag=True, help="enable verbose logging")
@click.argument("player_name")
def replay(api_key, shard, wins_only, latest, size, path, verbose, player_name):
    """Generate html replay(s) for a player's recent games.

    usage: $ chicken-dinner replay --api-key=$PUBG_API_KEY --shard=steam -lw -s 6 -p /path/to/my/replays
    usage: $ chicken-dinner replay --api-key=$PUBG_API_KEY --shard=steam --latest --wins-only --size=6 --path=/path/to/my/replays
    """
    if verbose:
        logger = logging.getLogger()
        logger.setLevel("INFO")
    pubg = get_pubg(api_key, shard)
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
            filename = os.path.join(
                path,
                player_name + "_" + match.created_at.replace("-", "").replace(":", "") + "_" + match_id + ".html"
            )
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
