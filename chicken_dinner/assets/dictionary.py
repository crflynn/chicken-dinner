"""Get the latest map images."""
import json
import logging
import os

import requests


logger = logging.getLogger()


DICTIONARY_URL = "https://api.github.com/repos/pubg/api-assets/contents/dictionaries/telemetry?ref=master"

DICTIONARY_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "assets",
    "dictionary.json"
)


def _get_items(url):
    response = requests.get(url).json()
    dictionary = {}
    for item in response:
        if item["type"] == "dir":
            logging.info("Traversing " + item["path"])
            dictionary.update(_get_items(item["url"]))
        elif item["path"].split(".")[-1] == "json":
            logging.info("Downloading " + item["path"])
            json_contents = requests.get(item["download_url"]).text
            dictionary.update(json.loads(json_contents))
    return dictionary


def update_dictionary():
    """Update the telemetry dictionary."""
    logger.setLevel("INFO")
    telemetry_dictionary = _get_items(DICTIONARY_URL)
    json.dump(telemetry_dictionary, open(DICTIONARY_PATH, "w"), indent=4)


if __name__ == "__main__":
    update_dictionary()
