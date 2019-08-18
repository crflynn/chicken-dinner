"""Get the latest map images."""
import logging
import os

import requests


logger = logging.getLogger()


MAPS_URL = "https://api.github.com/repos/pubg/api-assets/contents/Assets/Maps?ref=master"

MAP_ASSET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "assets", "maps")


def update_maps():
    """Update the maps local to this package."""
    logger.setLevel("INFO")
    response = requests.get(MAPS_URL).json()
    map_files = [f["download_url"] for f in response]

    for map_file in map_files:
        filename = map_file.split("/")[-1]
        logging.info("Downloading " + filename)

        response = requests.get(map_file)

        # Map names are inconsistent
        filename = filename.replace("Sanhok", "Savage")
        filename = filename.replace("Vikendi", "DihorOtok")
        filename = filename.replace("Miramar", "Desert")
        filename = filename.replace("Erangel_Remastered", "Baltic")
        filename = filename.replace("Camp_Jackal", "Range")
        path = os.path.join(MAP_ASSET_PATH, filename)

        with open(path, "wb") as img:
            logging.info("Saving " + path)
            img.write(response.content)


if __name__ == "__main__":
    update_maps()
