"""Function for generating playback animations."""
import logging
import os
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib import rc
from matplotlib.animation import FuncAnimation

from chicken_dinner.constants import COLORS
from chicken_dinner.constants import map_dimensions


rc("animation", embed_limit=100)


MAP_ASSET_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "assets",
    "maps"
)


def create_playback_animation(
        telemetry,
        filename="playback.html",
        labels=True,
        disable_labels_after=None,
        label_players=[],
        dead_players=True,
        dead_player_labels=False,
        zoom=False,
        zoom_edge_buffer=0.5,
        use_hi_res=False,
        color_teams=True,
        highlight_teams=[],
        highlight_players=[],
        highlight_color="#FFFF00",
        highlight_winner=False,
        label_highlights=True,
        care_packages=True,
        damage=True,
        end_frames=20,
        size=5,
        dpi=100,
        interpolate=True,
        interval=1,
        fps=30,
):
    """Create a playback animation from telemetry data.

    Using matplotlib's animation library, create an HTML5 animation saved to
    disk relying on external ``ffmpeg`` library to create the video.

    To view the animation, open the resulting file in your browser.

    :param telemetry: an Telemetry instance
    :param filename: a file to generate for the animation (default
        "playback.html")
    :param bool labels: whether to label players by name
    :param int disable_labels_after: if passed, turns off player labels
        after number of seconds elapsed in game
    :param list label_players: a list of strings of player names that
        should be labeled
    :param bool dead_players: whether to mark dead players
    :param list dead_player_labels: a list of strings of players that
        should be labeled when dead
    :param bool zoom: whether to zoom with the circles through the playback
    :param float zoom_edge_buffer: how much to buffer the blue circle edge
        when zooming
    :param bool use_hi_res: whether to use the hi-res image, best to be set
        to True when using zoom
    :param bool color_teams: whether to color code different teams
    :param list highlight_teams: a list of strings of player names whose
        teams should be highlighted
    :param list highlight_players: a list of strings of player names who
        should be highlighted
    :param str highlight_color: a color to use for highlights
    :param bool highlight_winner: whether to highlight the winner(s)
    :param bool label_highlights: whether to label the highlights
    :param bool care_packages: whether to show care packages
    :param bool damage: whether to show PvP damage
    :param int end_frames: the number of extra end frames after game has
        been completed
    :param int size: the size of the resulting animation frame
    :param int dpi: the dpi to use when processing the animation
    :param bool interpolate: use linear interpolation to get frames with
        second-interval granularity
    :param int interval: interval between gameplay frames in seconds
    :param int fps: the frames per second for the animation
    """

    # Extract data
    positions = telemetry.player_positions()
    circles = telemetry.circle_positions()
    rankings = telemetry.rankings()
    winner = telemetry.winner()
    killed = telemetry.killed()
    rosters = telemetry.rosters()
    damages = telemetry.player_damages()
    package_spawns = telemetry.care_package_positions(land=False)
    package_lands = telemetry.care_package_positions(land=True)
    map_id = telemetry.map_id()
    mapx, mapy = map_dimensions[map_id]
    all_times = []
    for player, pos in positions.items():
        for p in pos:
            all_times.append(int(p[0]))
    all_times = sorted(list(set(all_times)))

    if highlight_winner:
        for player in winner:
            highlight_players.append(player)
        highlight_players = list(set(highlight_players))

    if highlight_teams is not None:
        for team_player in highlight_teams:
            for team_id, roster in rosters.items():
                if team_player in roster:
                    for player in roster:
                        highlight_players.append(player)
                    break

        highlight_players = list(set(highlight_players))

    if label_highlights:
        for player in highlight_players:
            label_players.append(player)
    label_players = list(set(label_players))

    team_colors = None
    if color_teams:
        # Randomly select colors from the pre-defined palette
        colors = COLORS
        idx = list(range(len(colors)))
        random.shuffle(idx)
        team_colors = {}
        count = 0
        for team_id, roster in rosters.items():
            for player in roster:
                team_colors[player] = colors[idx[count]]
            count += 1

    # Get the max "frame number"
    maxlength = 0
    for player, pos in positions.items():
        try:
            if pos[-1][0] > maxlength:
                maxlength = pos[-1][0]
        except IndexError:
            continue

    if interpolate:
        maxlength = max(all_times)
    else:
        maxlength = max([maxlength, len(circles)])

    # Initialize the plot and artist objects
    fig = plt.figure(frameon=False, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    if use_hi_res:
        if map_id == "Savage_Main":
            map_image = map_id + ".png"
        else:
            map_image = map_id + ".jpg"
    else:
        map_image = map_id + "_lowres.jpg"
    img_path = os.path.join(MAP_ASSET_PATH, map_image)
    try:
        img = mpimg.imread(img_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            "High resolution images not included in package.\n"
            "Download images from https://github.com/pubg/api-assets/tree/master/Assets/Maps\n"
            "and place in folder: " + MAP_ASSET_PATH
        )
    ax.imshow(img, extent=[0, mapx, 0, mapy])

    players = ax.scatter(-10000, -10000, marker="o", c="w", edgecolor="k", s=60, linewidths=1, zorder=20)
    deaths = ax.scatter(-10000, -10000, marker="X", c="r", edgecolor="k", s=60, linewidths=1, alpha=0.5, zorder=10)

    if highlight_players or highlight_teams:
        highlights = ax.scatter(-10000, -10000, marker="*", c=highlight_color, edgecolor="k", s=180, linewidths=1, zorder=25)
        highlights_deaths = ax.scatter(-10000, -10000, marker="X", c=highlight_color, edgecolor="k", s=60, linewidths=1, zorder=15)

    if labels:
        if label_players is not None:
            name_labels = {
                player_name: ax.text(0, 0, player_name, size=8, zorder=19)
                for player_name in positions if player_name in label_players
            }
        else:
            name_labels = {
                player_name: ax.text(0, 0, player_name, size=8, zorder=19)
                for player_name in positions
            }
        for label in name_labels.values():
            label.set_path_effects([patheffects.withStroke(linewidth=2, foreground="w")])

    blue_circle = plt.Circle((0, 0), 0, edgecolor="b", linewidth=2, fill=False, zorder=5)
    white_circle = plt.Circle((0, 0), 0, edgecolor="w", linewidth=2, fill=False, zorder=6)
    red_circle = plt.Circle((0, 0), 0, color="r", edgecolor=None, lw=0, fill=True, alpha=0.3, zorder=7)

    care_package_spawns, = ax.plot(-10000, -10000, marker="s", c="w", markerfacecoloralt="w", fillstyle="bottom", mec="k", markeredgewidth=0.5, markersize=10, lw=0, zorder=8)
    care_package_lands, = ax.plot(-10000, -10000, marker="s", c="r", markerfacecoloralt="b", fillstyle="bottom", mec="k", markeredgewidth=0.5, markersize=10, lw=0, zorder=9)

    damage_slots = 50
    damage_lines = []
    for k in range(damage_slots):
        dline, = ax.plot(-10000, -10000, marker="x", c="r", mec="r", markeredgewidth=5, markersize=10, lw=2, markevery=[1], alpha=0.5, zorder=50)
        damage_lines.append(dline)

    ax.add_patch(blue_circle)
    ax.add_patch(white_circle)
    ax.add_patch(red_circle)

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.set_size_inches((size, size))

    ax.set_xlim([0, mapx])
    ax.set_ylim([0, mapy])

    # Frame init function
    def init():
        if labels:
            if highlight_players or highlight_teams:
                updates = players, deaths, highlights, highlights_deaths, blue_circle, red_circle, white_circle, *tuple(name_labels.values())
            else:
                updates = players, deaths, blue_circle, red_circle, white_circle, *tuple(name_labels.values())
        else:
            if highlight_players or highlight_teams:
                updates = players, deaths, highlights, highlights_deaths, blue_circle, red_circle, white_circle
            else:
                updates = players, deaths, blue_circle, red_circle, white_circle
        if care_packages:
            updates = *updates, care_package_lands, care_package_spawns
        if damage:
            updates = *updates, *damage_lines
        return updates

    def interpolate_coords(t, coords, tidx, vidx, step=False):
        inter = False
        for idx, coord in enumerate(coords):
            if coord[tidx] > t:
                inter = True
                break

        if not inter:
            return coords[-1][vidx]

        if idx == 0:
            return coords[0][vidx]
        else:
            v0 = coords[idx - 1][vidx]
            t0 = coords[idx - 1][tidx]

        v1 = coords[idx][vidx]
        t1 = coords[idx][tidx]

        if step:
            return v1
        else:
            return v0 + (t - t0) * (v1 - v0) / (t1 - t0)

    # Frame update function
    def update(frame):
        logging.info("Processing frame {frame}".format(frame=frame))
        try:
            if interpolate:
                blue_circle.center = (
                    interpolate_coords(frame, circles["blue"], 0, 1),
                    mapy - interpolate_coords(frame, circles["blue"], 0, 2))
                red_circle.center = (
                    interpolate_coords(frame, circles["red"], 0, 1, True),
                    mapy - interpolate_coords(frame, circles["red"], 0, 2, True))
                white_circle.center = (
                    interpolate_coords(frame, circles["white"], 0, 1, True),
                    mapy - interpolate_coords(frame, circles["white"], 0, 2, True))

                blue_circle.set_radius(
                    interpolate_coords(frame, circles["blue"], 0, 4))
                red_circle.set_radius(
                    interpolate_coords(frame, circles["red"], 0, 4, True))
                white_circle.set_radius(
                    interpolate_coords(frame, circles["white"], 0, 4, True))
            else:
                blue_circle.center = circles["blue"][frame][1], mapy - circles["blue"][frame][2]
                red_circle.center = circles["red"][frame][1], mapy - circles["red"][frame][2]
                white_circle.center = circles["white"][frame][1], mapy - circles["white"][frame][2]

                blue_circle.set_radius(circles["blue"][frame][4])
                red_circle.set_radius(circles["red"][frame][4])
                white_circle.set_radius(circles["white"][frame][4])
        except IndexError:
            pass

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        xwidth = xlim[1] - xlim[0]
        ywidth = ylim[1] - ylim[0]

        if zoom:
            try:
                if interpolate:
                    margin_offset = (1 + zoom_edge_buffer) * interpolate_coords(frame, circles["blue"], 0, 4)
                    xmin = max([0, interpolate_coords(frame, circles["blue"], 0, 1) - margin_offset])
                    xmax = min([mapx, interpolate_coords(frame, circles["blue"], 0, 1) + margin_offset])
                    ymin = max([0, mapy - interpolate_coords(frame, circles["blue"], 0, 2) - margin_offset])
                    ymax = min([mapy, mapy - interpolate_coords(frame, circles["blue"], 0, 2) + margin_offset])
                else:
                    margin_offset = (1 + zoom_edge_buffer) * circles["blue"][frame][4]
                    xmin = max([0, circles["blue"][frame][1] - margin_offset])
                    xmax = min([mapx, circles["blue"][frame][1] + margin_offset])
                    ymin = max([0, mapy - circles["blue"][frame][2] - margin_offset])
                    ymax = min([mapy, mapy - circles["blue"][frame][2] + margin_offset])

                # ensure full space taken by map
                if xmax - xmin >= ymax - ymin:
                    if ymin == 0:
                        ymax = ymin + (xmax - xmin)
                    elif ymax == mapy:
                        ymin = ymax - (xmax - xmin)
                else:
                    if xmin == 0:
                        xmax = xmin + (ymax - ymin)
                    elif xmax == mapx:
                        xmin = xmax - (ymax - ymin)

                ax.set_xlim([xmin, xmax])
                ax.set_ylim([ymin, ymax])

                xwidth = xmax - xmin
                ywidth = ymax - ymin
            except IndexError:
                pass

        positions_x = []
        positions_y = []
        highlights_x = []
        highlights_y = []
        deaths_x = []
        deaths_y = []
        highlights_deaths_x = []
        highlights_deaths_y = []
        care_package_lands_x = []
        care_package_lands_y = []
        care_package_spawns_x = []
        care_package_spawns_y = []

        if color_teams:
            marker_colors = []
            death_marker_colors = []
        else:
            marker_colors = "w"
            death_marker_colors = "r"

        t = 0
        damage_count = 0
        for player, pos in positions.items():
            try:
                player_max = pos[-1][0]
                # This ensures the alive winner(s) stay on the map at the end.
                if frame >= player_max and player not in winner:
                    raise IndexError
                elif frame >= player_max and player not in killed:
                    fidx = frame if interpolate else -1
                else:
                    fidx = frame

                if interpolate:
                    t = max([t, fidx])
                else:
                    t = max([t, pos[fidx][0]])

                for package in package_spawns:
                    if package[0] < t and package[0] > t - 60:
                        care_package_spawns_x.append(package[1])
                        care_package_spawns_y.append(mapy - package[2])
                for package in package_lands:
                    if package[0] < t:
                        care_package_lands_x.append(package[1])
                        care_package_lands_y.append(mapy - package[2])

                # Update player positions
                if interpolate:
                    if fidx >= pos[-1][0] and player in killed:
                        raise IndexError
                    x = interpolate_coords(fidx, pos, 0, 1)
                    y = mapy - interpolate_coords(fidx, pos, 0, 2)
                else:
                    x = pos[fidx][1]
                    y = mapy - pos[fidx][2]

                # Update player highlights
                if player in highlight_players:
                    highlights_x.append(x)
                    highlights_y.append(y)
                else:
                    positions_x.append(x)
                    positions_y.append(y)
                    # Set colors
                    if color_teams:
                        marker_colors.append(team_colors[player])

                # Update labels
                if labels and player in label_players:
                    if disable_labels_after is not None and frame >= disable_labels_after:
                        name_labels[player].set_position((-100000, -100000))
                    else:
                        name_labels[player].set_position((x + 10000 * xwidth / mapx, y - 10000 * ywidth / mapy))

                # Update player damages
                if damage:
                    try:
                        for attack in damages[player]:
                            damage_frame = int(attack[0])
                            if damage_frame >= fidx + interval:
                                break
                            elif damage_frame >= fidx and damage_frame < fidx + interval:
                                damage_line_x = [attack[1], attack[4]]
                                damage_line_y = [mapy - attack[2], mapy - attack[5]]
                                damage_lines[damage_count].set_data(damage_line_x, damage_line_y)
                                damage_count += 1
                    except KeyError:
                        pass

            except IndexError as exc:
                # Set death markers
                if player in highlight_players:
                    highlights_deaths_x.append(pos[-1][1])
                    highlights_deaths_y.append(mapy - pos[-1][2])
                else:
                    deaths_x.append(pos[-1][1])
                    deaths_y.append(mapy - pos[-1][2])

                    # Set death marker colors
                    if color_teams:
                        death_marker_colors.append(team_colors[player])

                # Draw dead players names
                if labels and dead_player_labels and player in label_players:
                    name_labels[player].set_position((pos[-1][1] + 10000 * xwidth / mapx, mapy - pos[-1][2] - 10000 * ywidth / mapy))
                    name_labels[player].set_path_effects([patheffects.withStroke(linewidth=1, foreground="gray")])
                # Offscreen if labels are off
                elif labels and player in label_players:
                    name_labels[player].set_position((-100000, -100000))

        player_offsets = [(x, y) for x, y in zip(positions_x, positions_y)]
        if len(player_offsets) > 0:
            players.set_offsets(player_offsets)
        else:
            players.set_offsets([(-100000, -100000)])

        if color_teams:
            players.set_facecolors(marker_colors)

        death_offsets = [(x, y) for x, y in zip(deaths_x, deaths_y)]
        if len(death_offsets) > 0:
            deaths.set_offsets(death_offsets)
        if color_teams:
            deaths.set_facecolors(death_marker_colors)

        if highlight_players is not None:
            highlight_offsets = [(x, y) for x, y in zip(highlights_x, highlights_y)]
            if len(highlight_offsets) > 0:
                highlights.set_offsets(highlight_offsets)
            else:
                highlights.set_offsets([(-100000, -100000)])

            highlight_death_offsets = [(x, y) for x, y in zip(highlights_deaths_x, highlights_deaths_y)]
            if len(highlight_death_offsets) > 0:
                highlights_deaths.set_offsets(highlight_death_offsets)

        if len(care_package_lands_x) > 0:
            care_package_lands.set_data(care_package_lands_x, care_package_lands_y)

        if len(care_package_spawns_x) > 0:
            care_package_spawns.set_data(care_package_spawns_x, care_package_spawns_y)

        # Remove the remaining slots
        for k in range(damage_count, damage_slots):
            damage_lines[k].set_data([], [])

        if labels:
            if highlight_players or highlight_teams:
                updates = players, deaths, highlights, highlights_deaths, blue_circle, red_circle, white_circle, *tuple(name_labels.values())
            else:
                updates = players, deaths, blue_circle, red_circle, white_circle, *tuple(name_labels.values())
        else:
            if highlight_players or highlight_teams:
                updates = players, deaths, highlights, highlights_deaths, blue_circle, red_circle, white_circle
            else:
                updates = players, deaths, blue_circle, red_circle, white_circle
        if care_packages:
            updates = *updates, care_package_lands, care_package_spawns
        if damage:
            updates = *updates, *damage_lines
        return updates

    # Create the animation
    animation = FuncAnimation(
        fig, update,
        frames=range(0, maxlength + end_frames, interval),
        interval=int(1000 / fps),
        init_func=init, blit=True,
    )

    # Write the html5 to buffer
    h5 = animation.to_html5_video()

    # Save to disk
    logging.info("Saving file: {file}".format(file=filename))
    with open(filename, "w") as f:
        f.write(h5)
    logging.info("Saved file.")

    return True
