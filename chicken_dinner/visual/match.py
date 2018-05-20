import json
import os
import random

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ImageMagickWriter
from matplotlib.animation import PillowWriter

from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.constants import COLORS


t = json.load(open("secret.json", "r"))

game = Telemetry.from_json(t)
positions = game.player_positions()
circles = game.circle_positions()
rosters = game.rosters()
team_size = max([len(v) for v in rosters.values()])
team_colors = None
if team_size > 1:
    colors = COLORS
    idx = list(range(len(colors)))
    random.shuffle(idx)
    team_colors = {}
    count = 0
    for team_id, roster in rosters.items():
        for player in roster:
            team_colors[player] = colors[idx[count]]
        count += 1
# print(json.dumps(game_states,indent=3))
# raise

ml = game.match_length()
print(game.map_name())
interval = 5
timestops = range(0, ml + interval, interval)

player_times = {}
times = {}
player_spacing = {}

maxlength = 0
for player, pos in positions.items():
    if len(pos) > maxlength:
        maxlength = len(pos)
maxlength = max([maxlength, len(circles)])

print(json.dumps(times, indent=3))


# def create_match_plot(telemetry, image_size=12):
fig = plt.figure(frameon=False, dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
img_path = os.path.join("chicken_dinner", "assets", "maps", "Erangel_Main_lowres.jpg")
img = mpimg.imread(img_path)
implot = ax.imshow(img, extent=[0, 819200, 0, 819200])

xdata = []
ydata = []
players = ax.scatter(0, 0, marker="o", c="w", edgecolor="k", s=15, linewidths=0.5)

blue_circle = plt.Circle((0, 0), 0, edgecolor="b", linewidth=1, fill=False)
white_circle = plt.Circle((0, 0), 0, edgecolor="w", linewidth=1, fill=False)
red_circle = plt.Circle((0, 0), 0, color="r", edgecolor=None, fill=True, alpha=0.3)
ax.add_patch(blue_circle)
ax.add_patch(white_circle)
ax.add_patch(red_circle)

fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
fig.set_size_inches((5, 5))

ax.set_xlim([0, 819200])
ax.set_ylim([0, 819200])



def init():
    return players, blue_circle, red_circle, white_circle

def update(frame):
    xdata = []
    ydata = []
    mfcdata = "w"

    if team_colors is not None:
        mfcdata = []
    else:
        mfcdata = "w"

    for player, pos in positions.items():
        try:
            xdata.append(pos[frame][1])
            ydata.append(819200 - pos[frame][2])
            if team_colors is not None:
                mfcdata.append(team_colors[player])
        except IndexError:
            continue

    offsets = [(x, y) for x, y in zip(xdata, ydata)]
    players.set_offsets(offsets)
    players.set_facecolors(mfcdata)

    try:
        blue_circle.center = circles["blue"][frame][1], 819200 - circles["blue"][frame][2]
        red_circle.center = circles["red"][frame][1], 819200 - circles["red"][frame][2]
        white_circle.center = circles["white"][frame][1], 819200 - circles["white"][frame][2]
        blue_circle.set_radius(circles["blue"][frame][4])
        red_circle.set_radius(circles["red"][frame][4])
        white_circle.set_radius(circles["white"][frame][4])
    except IndexError:
        pass

    return players, blue_circle, red_circle, white_circle

animation = FuncAnimation(
    fig, update,
    frames=range(maxlength),
    init_func=init, blit=True,
    # interval=250,
    repeat=True,
    repeat_delay=1000
)

h5 = animation.to_html5_video(embed_limit=100)

with open("secret.html", "w") as f:
    f.write(h5)
