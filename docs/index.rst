.. Chicken Dinner documentation master file, created by
   sphinx-quickstart on Sun May 20 20:12:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chicken Dinner
==============

Python PUBG JSON API Wrapper and playback visualizer.

Installation
------------

To install using pip:

.. code-block:: bash

    pip install chicken-dinner

To be able to generate playback visualizations, use:

.. code-block:: bash

    pip install chicken-dinner[visual]

Getting started
---------------

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


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    pubgapi/core
    pubgapi/pubg
    models/api
    models/match
    models/telemetry
    visual/playback
    assets/maps
    sample


Indices and tables
==================

* :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
