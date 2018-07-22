import json
import logging

from chicken_dinner.models.telemetry import Telemetry

logger = logging.getLogger()
logger.setLevel("INFO")

if __name__ == "__main__":
    # Load temp
t = json.load(open("test.json", "r"))
telemetry = Telemetry.from_json(t)
events = telemetry.events
    # print(type(t), len(t))
    # for e in events:
    #     print(e.event_type)
