import json
import logging

from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore

from .secret import api_key

logger = logging.getLogger()
logger.setLevel("DEBUG")

pubg = PUBG(api_key, "pc-tournament")
for k in range(6):
    tournaments = pubg.tournaments()
for k in range(5):
    print("t " + str(k))
    tournament = tournaments[k].response
