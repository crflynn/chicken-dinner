import json
import os
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib.animation import FuncAnimation

from chicken_dinner.constants import COLORS
from chicken_dinner.constants import map_dimensions


def create_match_animation(
        telemetry,
        filename,
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
        end_frames=20,
        size=5,
        dpi=200
    ):

    # Extract data
    positions = telemetry.player_positions()
    circles = telemetry.circle_positions()
    rankings = telemetry.rankings()
    winner = telemetry.winner()
    killed = telemetry.killed()
    rosters = telemetry.rosters()
    map_name = telemetry.map_name()
    mapx, mapy = map_dimensions[map_name]

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
    red_circle = plt.Circle((0, 0), 0, color="r", edgecolor=None, fill=True, alpha=0.3)

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
        return updates

    # Frame update function
    def update(frame):
        print(frame)
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

        if color_teams:
            marker_colors = []
            death_marker_colors = []
        else:
            marker_colors = "w"
            death_marker_colors = "r"

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

                # Update labels
                if labels and player in label_players:
                    if disable_labels_after is not None and frame >= disable_labels_after:
                        name_labels[player].set_position((-100000, -100000))
                    else:
                        name_labels[player].set_position((pos[fidx][1] + 10000 * xwidth/mapx, mapy - pos[fidx][2] - 10000 * ywidth/mapy))

                # Set colors
                if color_teams:
                    marker_colors.append(team_colors[player])
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
    with open(filename, "w") as f:
        f.write(h5)

    return True
