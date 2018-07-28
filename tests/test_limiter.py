import json
import logging

from .secret import api_key

from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG

logger = logging.getLogger()
logger.setLevel("DEBUG")

pubg = PUBG(api_key, "pc-tournament")
for k in range(6):
    tournaments = pubg.tournaments()
for k in range(5):
    print("t " + str(k))
    tournament = tournaments[k].response
