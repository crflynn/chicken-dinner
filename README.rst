Chicken Dinner
==============

Python PUBG JSON API Wrapper and playback visualizer.

Installation
------------

To install using pip:

.. code-block:: bash

    pip install chicken-dinner

To use the playback visualization you will also need ffmpeg. You can install
on Mac OSX using brew.

.. code-block:: bash

    brew install ffmpeg

Usage
-----

Working with the low-level API class.

.. code-block:: python

    from chicken_dinner.pubgapi import PUBGCore

    api_key = "your_api_key"
    pubgcore = PUBGCore(api_key, "pc-na")
    shroud = pubgcore.players("player_names", "shroud")
    print(shroud)

    # {'data': [{'type': 'player', 'id': 'account.d50f...

Working with the high-level API class.

.. code-block:: python

    from chicken_dinner.pubgapi import PUBG

    api_key = "your_api_key"
    pubg = PUBG(api_key, "pc-na")
    shroud = pubg.players_from_names("shroud")[0]
    shroud_season = shroud.get_current_season()
    squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")
    print(squad_fpp_stats)

    # {'assists': 136, 'boosts': 313, 'dbnos': 550, 'daily_kills':...

Visualizing telemetry data

.. code-block:: python

    from chicken_dinner.pubgapi import PUBG

    api_key = "your_api_key"
    pubg = PUBG(api_key, "pc-na")
    shroud = pubg.players_from_names("shroud")[0]
    recent_match_id = shroud.match_ids[0]
    recent_match = pubg.match(recent_match_id)
    recent_match_telemetry = recent_match.get_telemetry()
    recent_match_telemetry.create_playback_animation("recent_match.html")
