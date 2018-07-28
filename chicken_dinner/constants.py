"""Constants and reference maps from pythonic names to pubg api names."""
import json

from chicken_dinner.assets.dictionary import DICTIONARY_PATH


PERSPECTIVES = ("tpp", "fpp")
GROUPS = ("solo", "duo", "squad")

gp_to_game_mode = {
    "solo": "solo",
    "duo": "duo",
    "squad": "squad",
    "solo-fpp": "solo-fpp",
    "duo-fpp": "duo-fpp",
    "squad-fpp": "squad-fpp",
}
game_mode_to_gp = {
    "solo": "solo",
    "duo": "duo",
    "squad": "squad",
    "solo-fpp": "solo-fpp",
    "duo-fpp": "duo-fpp",
    "squad-fpp": "squad-fpp",
}
gp_to_matches = {
    "solo": "matchesSolo",
    "duo": "matchesDuo",
    "squad": "matchesSquad",
    "solo-fpp": "matchesSoloFPP",
    "duo-fpp": "matchesDuoFPP",
    "squad-fpp": "matchesSquadFPP",
}
matches_to_gp = {
    "matchesSolo": "solo",
    "matchesDuo": "duo",
    "matchesSquad": "squad",
    "matchesSoloFPP": "solo-fpp",
    "matchesDuoFPP": "duo-fpp",
    "matchesSquadFPP": "squad-fpp",
}

map_to_map_name = {
    "Desert_Main": "Miramar",
    "Erangel_Main": "Erangel",
    "Savage_Main": "Sanhok",
}

map_name_to_map = {
    "Miramar": "Desert_Main",
    "Erangel": "Erangel_Main",
    "Sanhok": "Savage_Main",
}

map_dimensions = {
    "Desert_Main": [819200, 819200],
    "Erangel_Main": [819200, 819200],
    "Savage_Main": [409600, 409600],
}

true_false = {
    "false": False,
    "true": True,
}

asset_map = json.load(open(DICTIONARY_PATH, "r"))

BASE_URL = "https://api.playbattlegrounds.com"
SHARD_URL = BASE_URL + "/shards/"
STATUS_URL = BASE_URL + "/status"
TOURNAMENTS_URL = BASE_URL + "/tournaments"
PLAYER_FILTERS = {
    "player_ids": "playerIds",
    "player_names": "playerNames",
}
SHARDS = [
    "xbox-as",
    "xbox-eu",
    "xbox-na",
    "xbox-oc",
    "pc-krjp",
    "pc-jp",
    "pc-na",
    "pc-eu",
    "pc-oc",
    "pc-kakao",
    "pc-sea",
    "pc-sa",
    "pc-as",
    "pc-tournament",
]

COLORS = [
    "#fc3f3f",
    "#d93636",
    "#eb7575",
    "#eb583b",
    "#fc937e",
    "#d97e6c",
    "#eb753b",
    "#fca87e",
    "#d9916c",
    "#eb933b",
    "#ebb075",
    "#fcbd3f",
    "#d9a336",
    "#ebc475",
    "#fcdd3f",
    "#d9be36",
    "#fce77e",
    "#d9c76c",
    "#ebeb3b",
    "#fcfc7e",
    "#d9d96c",
    "#ddfc3f",
    "#bed936",
    "#d7eb75",
    "#bdfc3f",
    "#a3d936",
    "#d2fc7e",
    "#b5d96c",
    "#9efc3f",
    "#87d936",
    "#bdfc7e",
    "#a3d96c",
    "#7efc3f",
    "#6cd936",
    "#a8fc7e",
    "#91d96c",
    "#58eb3b",
    "#89eb75",
    "#3ffc3f",
    "#7efc7e",
    "#6cd96c",
    "#3beb58",
    "#7efc93",
    "#6cd97e",
    "#3ffc7e",
    "#36d96c",
    "#7efca8",
    "#6cd991",
    "#3beb93",
    "#7efcbd",
    "#6cd9a3",
    "#3ffcbd",
    "#36d9a3",
    "#75ebc4",
    "#3bebcd",
    "#7efce7",
    "#6cd9c7",
    "#3ffcfc",
    "#36d9d9",
    "#7efcfc",
    "#6cd9d9",
    "#3fddfc",
    "#36bed9",
    "#7ee7fc",
    "#6cc7d9",
    "#3fbdfc",
    "#36a3d9",
    "#7ed2fc",
    "#6cb5d9",
    "#3f9efc",
    "#3687d9",
    "#7ebdfc",
    "#6ca3d9",
    "#3f7efc",
    "#366cd9",
    "#759ceb",
    "#3b58eb",
    "#7e93fc",
    "#6c7ed9",
    "#3636d9",
    "#7e7efc",
    "#5f3ffc",
    "#937efc",
    "#7e6cd9",
    "#7e3ffc",
    "#6c36d9",
    "#9c75eb",
    "#9e3ffc",
    "#8736d9",
    "#bd7efc",
    "#a36cd9",
    "#bd3ffc",
    "#a336d9",
    "#d27efc",
    "#b56cd9",
    "#dd3ffc",
    "#be36d9",
    "#e77efc",
    "#c76cd9",
    "#fc3ffc",
    "#d936d9",
    "#fc7efc",
    "#d96cd9",
    "#eb3bcd",
    "#fc7ee7",
    "#d96cc7",
    "#fc3fbd",
    "#d936a3",
    "#fc7ed2",
    "#d96cb5",
    "#eb3b93",
    "#eb75b0",
    "#fc3f7e",
    "#d9366c",
    "#eb759c",
    "#fc3f5f",
    "#d93651",
    "#fc7e93",
    "#d96c7e",
]
