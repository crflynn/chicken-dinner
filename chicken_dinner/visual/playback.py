import json
import logging
import os
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import AnnotationBbox
from matplotlib.offsetbox import OffsetImage

from chicken_dinner.constants import COLORS
from chicken_dinner.constants import map_dimensions


def create_playback_animation(
        telemetry,
        filename="playback.html",
        labels=True,
        disable_labels_after=None,
        label_players=None,
        dead_players=True,
        dead_player_labels=False,
        zoom=False,
        zoom_edge_buffer=0.5,
        use_hi_res=False,
        color_teams=True,
        highlight_teams=None,
        highlight_players=None,
        highlight_color="#FFFF00",
        highlight_winner=False,
        label_highlights=True,
        care_packages=True,
        end_frames=20,
        size=5,
        dpi=200
    ):
    """Create a playback animation from telemetry data.

    Using matplotlib's animation library, create an HTML5 animation saved to
    disk relying on external ``ffmpeg`` library to create the video.

    To view the animation, open the resulting file in your browser.

    :param telemetry: an Telemetry instance
    :param filename: a file to generate for the animation (default
        "playback.html")
    :param bool labels: whether to label players by name
    :param int disable_labels_after: if passed, turns off player labels after
        number of seconds elapsed in game
    :param list label_players: a list of strings of player names that should
        be labeled
    :param bool dead_players: whether to mark dead players
    :param list dead_player_labels: a list of strings of players that should
        be labeled when dead
    :param bool zoom: whether to zoom with the circles through the playback
    :param float zoom_edge_buffer: how much to buffer the blue circle edge
        when zooming
    :param bool use_hi_res: whether to use the hi-res image, best to be set
        to True when using zoom
    :param bool color_teams: whether to color code different teams
    :param list highlight_teams: a list of strings of player names whose teams
        should be highlighted
    :param list highlight_players: a list of strings of player names who
        should be highlighted
    :param str highlight_color: a color to use for highlights
    :param bool highlight_winner: whether to highlight the winner(s)
    :param bool label_highlights: whether to label the highlights
    :param bool care_packages: whether to show care packages
    :param int end_frames: the number of extra end frames after game has been
        completed
    :param int size: the size of the resulting animation frame
    :param int dpi: the dpi to use when processing the animation
    """

    # Extract data
    positions = telemetry.player_positions()
    circles = telemetry.circle_positions()
    rankings = telemetry.rankings()
    winner = telemetry.winner()
    killed = telemetry.killed()
    rosters = telemetry.rosters()
    # package_spawns = telemetry.care_package_positions(land=False)
    package_lands = telemetry.care_package_positions(land=True)
    map_name = telemetry.map_name()
    mapx, mapy = map_dimensions[map_name]

    if highlight_winner:
        if highlight_players is None:
            highlight_players = []
        for player in winner:
            highlight_players.append(player)
        highlight_players = list(set(highlight_players))


    if highlight_teams is not None:
        if highlight_players is None:
            highlight_players = []
        for team_player in highlight_teams:
            for team_id, roster in rosters.items():
                if team_player in roster:
                    for player in roster:
                        highlight_players.append(player)
                    break

        highlight_players = list(set(highlight_players))

    if label_highlights:
        if label_players is None:
            label_players = []
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
        if len(pos) > maxlength:
            maxlength = len(pos)
    maxlength = max([maxlength, len(circles)])

    # Initialize the plot and artist objects
    fig = plt.figure(frameon=False, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    if use_hi_res:
        map_image = map_name + ".jpg"
    else:
        map_image = map_name + "_lowres.jpg"
    img_path = os.path.join("chicken_dinner", "assets", "maps", map_image)
    img = mpimg.imread(img_path)
    implot = ax.imshow(img, extent=[0, mapx, 0, mapy])

    xdata = []
    ydata = []
    players = ax.scatter(-10000, -10000, marker="o", c="w", edgecolor="k", s=15, linewidths=0.5)
    deaths = ax.scatter(-10000, -10000, marker="X", c="r", edgecolor="k", s=15, linewidths=0.5, alpha=0.5)
    if highlight_players or highlight_teams:
        highlights = ax.scatter(-10000, -10000, marker="*", c=highlight_color, edgecolor="k", s=45, linewidths=0.5)
        highlights_deaths = ax.scatter(-10000, -10000, marker="X", c=highlight_color, edgecolor="k", s=15, linewidths=0.5)

    if labels:
        if label_players is not None:
            name_labels = {
                player_name: ax.text(0, 0, player_name, size=4)
                for player_name in positions if player_name in label_players
            }
        else:
            name_labels = {
                player_name: ax.text(0, 0, player_name, size=4)
                for player_name in positions
            }
        for label in name_labels.values():
            label.set_path_effects([patheffects.withStroke(linewidth=1, foreground='w')])

    blue_circle = plt.Circle((0, 0), 0, edgecolor="b", linewidth=1, fill=False)
    white_circle = plt.Circle((0, 0), 0, edgecolor="w", linewidth=1, fill=False)
    red_circle = plt.Circle((0, 0), 0, color="r", edgecolor=None, lw=0, fill=True, alpha=0.3)

    care_package_lands, = ax.plot(-10000, -10000, marker="s", c="r", markerfacecoloralt="b", fillstyle="bottom", mec="k", markeredgewidth=0.25, markersize=5, lw=0)

    ax.add_patch(blue_circle)
    ax.add_patch(white_circle)
    ax.add_patch(red_circle)

    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
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
            updates = *updates, care_package_lands
        return updates

    # Frame update function
    def update(frame):
        logging.info("Processing frame {frame}".format(frame=frame))
        try:
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

        if color_teams:
            marker_colors = []
            death_marker_colors = []
        else:
            marker_colors = "w"
            death_marker_colors = "r"

        t = 0
        for player, pos in positions.items():
            try:
                # This ensures the alive winner(s) stay on the map at the end.
                if frame >= maxlength and player not in winner:
                    raise IndexError
                elif frame >= maxlength and player not in killed:
                    fidx = -1
                else:
                    fidx = frame

                # Update player positions
                if player in highlight_players:
                    highlights_x.append(pos[fidx][1])
                    highlights_y.append(mapy - pos[fidx][2])
                else:
                    positions_x.append(pos[fidx][1])
                    positions_y.append(mapy - pos[fidx][2])
                    # Set colors
                    if color_teams:
                        marker_colors.append(team_colors[player])

                # Update labels
                if labels and player in label_players:
                    if disable_labels_after is not None and frame >= disable_labels_after:
                        name_labels[player].set_position((-100000, -100000))
                    else:
                        name_labels[player].set_position((pos[fidx][1] + 10000 * xwidth/mapx, mapy - pos[fidx][2] - 10000 * ywidth/mapy))

                t = max([t, pos[fidx][0]])
                for package in package_lands:
                    if package[0] < t:
                        care_package_lands_x.append(package[1])
                        care_package_lands_y.append(mapy - package[2])
            except IndexError:
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
                    name_labels[player].set_position((pos[-1][1] + 10000 * xwidth/mapx, mapy - pos[-1][2] - 10000 * ywidth/mapy))
                    name_labels[player].set_path_effects([patheffects.withStroke(linewidth=1, foreground='gray')])
                # Offscreen if labels are off
                elif player in label_players:
                    name_labels[player].set_position((-100000, -100000))

        player_offsets = [(x, y) for x, y in zip(positions_x, positions_y)]
        if len(player_offsets) > 0:
            players.set_offsets(player_offsets)
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

            highlight_death_offsets = [(x, y) for x, y in zip(highlights_deaths_x, highlights_deaths_y)]
            if len(highlight_death_offsets) > 0:
                highlights_deaths.set_offsets(highlight_death_offsets)

        if len(care_package_lands_x) > 0:
            care_package_lands.set_data(care_package_lands_x, care_package_lands_y)

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
            updates = *updates, care_package_lands
        return updates

    # Create the animation
    animation = FuncAnimation(
        fig, update,
        frames=range(maxlength + end_frames),
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
