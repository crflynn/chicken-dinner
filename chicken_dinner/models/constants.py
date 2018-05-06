"""Constants and reference maps from pythonic names to pubg api names."""


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
}

true_false = {
    "false": False,
    "true": True,
}
