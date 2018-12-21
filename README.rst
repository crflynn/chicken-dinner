Chicken Dinner
==============

|rtd| |pypi| |pyversions|

.. |rtd| image:: https://img.shields.io/readthedocs/chicken-dinner.svg
    :target: http://chicken-dinner.readthedocs.io/en/latest/

.. |pypi| image:: https://img.shields.io/pypi/v/chicken-dinner.svg
    :target: https://pypi.python.org/pypi/chicken-dinner

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/chicken-dinner.svg
    :target: https://pypi.python.org/pypi/chicken-dinner

Python PUBG JSON API Wrapper and (optional) playback visualizer.

Samples
-------

* `Erangel - squads <http://chicken-dinner.readthedocs.io/en/latest/sample_erangel.html>`_
* `Miramar - solos <http://chicken-dinner.readthedocs.io/en/latest/sample_miramar.html>`_
* `Sanhok - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_sanhok.html>`_
* `Vikendi - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_vikendi.html>`_

Installation
------------

To install chicken-dinner, use pip. This will install the core dependencies
(``requests`` library) which provide functionality to the API wrapper classes.

.. code-block:: bash

    pip install chicken-dinner

To use the playback visualizations you will need to install the library with
extra dependencies for plotting (``matplotlib`` and ``pillow``).
For this you can also use pip:

.. code-block:: bash

    pip install chicken-dinner[visual]

To generate the animations you will also need ``ffmpeg`` installed on your
machine. On Max OSX you can install ``ffmpeg`` using brew.

.. code-block:: bash

    brew install ffmpeg

You can install ffmpeg on other systems from `here <https://www.ffmpeg.org/download.html>`_.

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
    recent_match_telemetry.playback_animation("recent_match.html")

Recommended playback settings:

.. code-block:: python

    telemetry.playback_animation(
        "match.html",
        zoom=True,
        labels=True,
        label_players=[],
        highlight_winner=True,
        label_highlights=True,
        size=6,
        end_frames=60,
        use_hi_res=False,
        color_teams=True,
        interpolate=True,
        damage=True,
        interval=2,
        fps=30,
    )

See the `documentation <http://chicken-dinner.readthedocs.io>`_ for more
details.
