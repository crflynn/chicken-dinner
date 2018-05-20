import json
import os

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ImageMagickWriter
from matplotlib.animation import PillowWriter

from chicken_dinner.models.telemetry import Telemetry


t = json.load(open("secret.json", "r"))

game = Telemetry.from_json(t)
positions = game.player_positions()
circles = game.circle_positions()
# print(json.dumps(game_states,indent=3))

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
    # for ts in timestops:
    #     if pos[-1][0] > ts:
    #         if ts not in times:
    #             times[ts] = 0
    #         times[ts] += 1

print(json.dumps(times, indent=3))


# def create_match_plot(telemetry, image_size=12):
fig, ax = plt.subplots(dpi=200)
xdata = []
ydata = []
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
img_path = os.path.join("chicken_dinner", "assets", "maps", "Erangel_Main_lowres.jpg")
img = mpimg.imread(img_path)
implot = plt.imshow(img, extent=[0, 819200, 0, 819200])
players, = plt.plot([], [], 'wo', mec='k', markersize=5)
blue_circle = plt.Circle((400000,400000), 40000, ec='b', lw=2, fill=False)
white_circle = plt.Circle((400000,400000), 40000, ec='w', lw=2, fill=False)
red_circle = plt.Circle((400000,400000), 40000, color='r', ec=None, fill=True, alpha=0.3)
ax.add_patch(blue_circle)
ax.add_patch(white_circle)
ax.add_patch(red_circle)
fig.set_size_inches((5, 5))

def init():
    return players, blue_circle, red_circle, white_circle

def update(frame):
    xdata=[]
    ydata=[]
    for player, pos in positions.items():
        try:
            xdata.append(pos[frame][1])
            ydata.append(819200 - pos[frame][2])
        except IndexError:
            continue
    players.set_data(xdata, ydata)
    try:
        blue_circle.center = circles["blue"][frame][1], 819200 - circles["blue"][frame][2]
        red_circle.center = circles["red"][frame][1], 819200 - circles["red"][frame][2]
        white_circle.center = circles["white"][frame][1], 819200 - circles["white"][frame][2]
        blue_circle.set_radius(circles["blue"][frame][3])
        red_circle.set_radius(circles["red"][frame][3])
        white_circle.set_radius(circles["white"][frame][3])
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
# matplotlib.rcParams["animation.bitrate"] = 3000
h5 = animation.to_html5_video(embed_limit=100)
# h5 = animation.to_jshtml(30)
with open("secret.html", "w") as f:
    f.write(h5)



# animation.save('secret.gif', writer=writer)
# animation.save("secret.gif")
# animation.to_html5_video()
# moviewriter = PillowWriter()
# moviewriter = ImageMagickFileWriter()
# with moviewriter.saving(fig, 'secret.gif', dpi=100):
#     init()
#     for j in range(20):
#         update(10000*j)
#         moviewriter.grab_frame()
#
# plt.show()
# plt.savefig("secret.png")
