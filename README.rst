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

Also includes basic CLI functionality for replays, leaderboards, stats, and updating assets.

Samples
-------

* `Erangel - squads <http://chicken-dinner.readthedocs.io/en/latest/sample_erangel.html>`_
* `Miramar - solos <http://chicken-dinner.readthedocs.io/en/latest/sample_miramar.html>`_
* `Sanhok - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_sanhok.html>`_
* `Vikendi - solos <http://chicken-dinner.readthedocs.io/en/latest/sample_vikendi.html>`_

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

CLI
---

For CLI commands using the PUBG API, an API Key is required.
You may provide the API key via an environment variable
named ``PUBG_API_KEY`` or with the CLI option ``--api-key``

.. code-block:: bash

    export PUBG_API_KEY=your_pubg_api_key
    chicken-dinner [command] --shard=steam ...

OR

.. code-block:: bash

    chicken-dinner [command] --api-key=your_pubg_api_key --shard=steam ...

A shard is optional, but the default shard is ``steam``.


Assets
~~~~~~

To update local assets, including hi-res maps and asset dictionaries:

.. code-block:: bash

    chicken-dinner assets


Leaderboards
~~~~~~~~~~~~

Display the leaderboards for a game mode (shard default is steam):

.. code-block:: bash

    chicken-dinner leaderboard --shard=steam solo-fpp


Player Stats
~~~~~~~~~~~~

Display player stats for lifetime or the current season (shard default is steam):

.. code-block:: bash

    # Get the lifetime stats for chocoTaco in solo-fpp
    chicken-dinner stats --shard=steam --lifetime --group=solo --perspective=fpp chocoTaco

    # Get the latest season stats for chocoTaco in solo-fpp
    chicken-dinner stats -g solo -p fpp chocoTaco

Replays
~~~~~~~

Generate html5 replays for matches (shard default is steam):

.. code-block:: bash

    # Generate a replay for the latest win of chocoTaco in specified path
    chicken-dinner replay --latest --wins-only --size=6 --path=/path/to/my/replays chocoTaco

    # Generate a replay for the latest game of chocoTaco
    chicken-dinner replay -l chocoTaco

    # Generate a replay for all of chocoTaco's wins in recent games
    chicken-dinner replay -w chocoTaco

    # Generate a replay for all of the recent games of chocoTaco
    chicken-dinner replay chocoTaco


More Examples
-------------

Setup
~~~~~

Creating a ``PUBG`` instance.

.. code-block:: python

    from chicken_dinner.pubgapi import PUBG

    api_key = "my_api_key"
    pubg = PUBG(api_key=api_key, shard="steam")


Player Examples
~~~~~~~~~~~~~~~

Getting information for a player by their name.

.. code-block:: python

    # Creates a Players instance (iterable Player instances)
    players = pubg.players_from_names("chocoTaco")

    # Take the first Player instance from the iterable
    chocotaco = players[0]

    chocotaco.name
    # chocoTaco

    chocotaco.match_ids
    # ['e0b3cb15-929f-4b42-8873-68a8f9998d2b', 'dd25cf69-77f1-4791-9b14-657e904d3534'...

    chocotaco.id
    # 'account.15cbf322a9bc45e88b0cd9f12ef4188e'

    chocotaco.url
    # 'https://api.playbattlegrounds.com/shards/steam/players/account.15cbf322a9bc45e88b0cd9f12ef4188e'


Or get the player instance from the id.

.. code-block:: python

    # Creates a Players instance (iterable Player instances)
    players = pubg.players_from_ids("account.15cbf322a9bc45e88b0cd9f12ef4188e")

    # Take the first Player instance from the iterable
    chocotaco = players[0]


Get information about multiple players and matches that they participated together.

.. code-block:: python

    # Creates a Players instance (iterable of Player instances)
    players = pubg.players_from_names(["shroud", "chocoTaco"])

    players.ids
    # ['account.d50fdc18fcad49c691d38466bed6f8fd', 'account.15cbf322a9bc45e88b0cd9f12ef4188e']

    players.names_to_ids()
    # {'shroud': 'account.d50fdc18fcad49c691d38466bed6f8fd', 'chocoTaco': 'account.15cbf322a9bc45e88b0cd9f12ef4188e'}

    players.ids_to_names()
    # {'account.d50fdc18fcad49c691d38466bed6f8fd': 'shroud', 'account.15cbf322a9bc45e88b0cd9f12ef4188e': 'chocoTaco'}

    players.shared_matches()
    # ['e0b3cb15-929f-4b42-8873-68a8f9998d2b', 'dd25cf69-77f1-4791-9b14-657e904d3534'...

    shroud = players[0]
    chocotaco = players[1]

Season Examples
~~~~~~~~~~~~~~~

Get an iterable of ``Seasons`` objects

.. code-block:: python

    seasons = pubg.seasons()

    seasons.ids
    # ['division.bro.official.2017-beta', 'division.bro.official.2017-pre1'...

    # Get the current season
    current_season = seasons.current()


Work with a ``Season`` instance

.. code-block:: python

    season = pubg.current_season()

    season.id
    # 'division.bro.official.pc-2018-04'

    season.is_current()
    # True

    season.is_offseason()
    # False

    # Get a player-season for a specific player
    chocotaco_season = season.get_player("account.15cbf322a9bc45e88b0cd9f12ef4188e")


Getting information about a player-season

.. code-block:: python

    # Using the factory instance directly
    chocotaco_season = pubg.player_season("account.15cbf322a9bc45e88b0cd9f12ef4188e", "division.bro.official.pc-2018-04")

    # Using a season
    season = pubg.current_season()
    chocotaco_season = season.get_player("account.15cbf322a9bc45e88b0cd9f12ef4188e")

    # Using a player
    chocotaco = pubg.players_from_names("chocoTaco")[0]
    chocotaco_season = chocotaco.get_season("division.bro.official.pc-2018-04")

    chocotaco_season.id
    # {'player_id': 'account.15cbf322a9bc45e88b0cd9f12ef4188e', 'season_id': 'division.bro.official.pc-2018-04'}

    chocotaco_season.player_id
    # 'account.15cbf322a9bc45e88b0cd9f12ef4188e'

    chocotaco_season.season_id
    # 'division.bro.official.pc-2018-04'

    chocotaco_season.match_ids("solo", "fpp")
    # ['4b0c5898-7149-4bcc-8da7-df4cdc07fd80', 'b26880e5-916d-4be8-abd7-45d8dddb6df3'...

    chocotaco_season.game_mode_stats("solo", "fpp")
    # {'assists': 38, 'boosts': 498, 'dbnos': 0, 'daily_kills': 18, 'daily_wins': 0, 'damage_dealt': 95036.79...


Leaderboards
~~~~~~~~~~~~


Leaderboards give the top 25 players for a particular game mode.

.. code-block:: python

    solo_fpp_leaderboard = pubg.leaderboard("solo-fpp")

    solo_fpp_leaderboard.game_mode
    # 'solo-fpp'

    solo_fpp_leaderboard.ids
    # ['account.cfb13f65d5d1452294efbe7e730f7b1c', 'account.9affa4ff8e5746bbb6a199f1a773c659'...

    solo_fpp_leaderboard.names
    # ['HuYa-17152571', 'Huya_15007597_LS', 'Douyu-7250640', 'Douyu-4778209', 'DouYu-1673291'...

    solo_fpp_leaderboard.ids_to_names()
    # {'account.f897d4a4b22f45cb8a85008039f5069e': 'HuYaTv-19488958', 'account.8ca07daf6c084dea81aacc00616fde9c': 'Breukin224'...

    solo_fpp_leaderboard.names_to_ids()
    # {'HuYaTv-19488958': 'account.f897d4a4b22f45cb8a85008039f5069e', 'Breukin224': 'account.8ca07daf6c084dea81aacc00616fde9c'...

    # Info about a player at particular rank
    solo_fpp_leaderboard.name(1)
    # 'HuYa-17152571'

    solo_fpp_leaderboard.id(1)
    # 'account.cfb13f65d5d1452294efbe7e730f7b1c'

    solo_fpp_leaderboard.stats(1)
    # {'rank_points': 6344, 'wins': 82, 'games': 1591, 'win_ratio': 0.0515399128, 'average_damage': 247, 'kills': 3218...

    # Get a player object for a player at rank 1
    player = solo_fpp_leaderboard.get_player(1)

Samples
~~~~~~~

Get randomly sampled match ids.

.. code-block:: python

    samples = pubg.samples()

    samples.match_ids
    # ['98192d81-8700-4e28-981d-00b14dfbb3c9', '7ce51ef0-6f73-4974-9bb6-532dec58355d'...


API Status
~~~~~~~~~~

Get the current API status

.. code-block:: python

    status = pubg.status()

    status.id
    # 'pubg-api'

    # Refreshes the API status
    status.refresh()

Matches
~~~~~~~

Get match information

.. code-block:: python

    match = pubg.match("e0b3cb15-929f-4b42-8873-68a8f9998d2b")

    match.asset_id
    # '44b787fd-c153-11e9-8b6c-0a586467d436'

    match.created_at
    # '2019-08-18T00:29:00Z'

    match.duration
    # 1686

    match.game_mode
    # 'duo-fpp'

    match.id
    # 'e0b3cb15-929f-4b42-8873-68a8f9998d2b'

    match.is_custom
    # False

    match.map_id
    # 'Baltic_Main'

    match.map_name
    # 'Erangel (Remastered)'

    match.rosters_player_names
    # {'9354f12b-8e79-4ca2-9465-6bdfa6b4bca9': ['Vealzor', 'Colin630'], 'c2eb2ecf-96d5-42c3-b0cb-49d734a716a6': ['KillaCon', 'FriendlyOrc']...

    match.telemetry_url
    # 'https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/steam/2019/08/18/00/58/44b787fd-c153-11e9-8b6c-0a586467d436-telemetry.json'

    match.url
    # 'https://api.playbattlegrounds.com/shards/steam/matches/e0b3cb15-929f-4b42-8873-68a8f9998d2b'

Get rosters and associated participants

.. code-block:: python

    # Get rosters
    rosters = match.rosters

    # Get single roster
    roster = rosters[0]

    roster.player_ids
    # ['account.7046d72ec24e45a7b0282d390dea91e5', 'account.9a154840c7db4f7f88def5198b9393b6']

    roster.player_names
    # ['Vealzor', 'Colin630']

    roster.stats
    # {'rank': 44, 'team_id': 12, 'won': 'false'}

    roster.won
    # False

    # Participant from a roster
    roster_participants = roster.participants
    participant = roster_participant[0]

    participant.name
    # 'Vealzor'

    participant.player_id
    # 'account.7046d72ec24e45a7b0282d390dea91e5'

    participant.stats
    # {'dbnos': 1, 'assists': 0, 'boosts': 0, 'damage_dealt': 113.032738...

    participant.teammates_player_ids
    # ['account.9a154840c7db4f7f88def5198b9393b6']

    participant.teammates_player_names
    # ['Colin630']

    participant.won
    # False

    # Get Participant instances for teammates
    teammates = participant.teammates

Get all Participants from Match

.. code-block:: python

    match_participants = match.participants


Telemetry
~~~~~~~~~

Get a Telemetry instance from a particular match

.. code-block:: python

    # Using the PUBG instance
    url = 'https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/steam/2019/08/18/00/58/44b787fd-c153-11e9-8b6c-0a586467d436-telemetry.json'
    telemetry = pubg.telemetry(url)

    # Using a Match instance
    match = pubg.match("e0b3cb15-929f-4b42-8873-68a8f9998d2b")
    telemetry = match.get_telemetry()

    # All available event types
    telemetry.event_types()
    # ['log_armor_destroy', 'log_care_package_land', 'log_care_package_spawn', 'log_game_state_periodic', 'log_heal'...

    # All specific events
    care_package_lands = telemetry.filter_by("log_care_package_land")

    telemetry.map_id()
    # 'Baltic_Main'

    telemetry.map_name()
    # 'Erangel (Remastered)'

    telemetry.num_players()
    # 100

    telemetry.num_teams()
    # 50

    telemetry.platform
    # 'pc'

    # Generates an HTML5 animation with ffmpeg
    telemetry.playback_animation("match.html")

    # Many more functions related to positions, circles, damages. Refer to docs


Telemetry events and objects are generic class wrappers. They are constructed
when the Telemetry instance is created. This makes them telemetry version-agnostic,
but requires some work to inspect their contents and structure. The TelemetryEvent
and TelemetryObject classes also transform the payload keys to snake_case.

TelemetryEvents are containers for event key-values and structures which contain a
hierarchy of TelemetryObjects.

`Telemetry Events <https://documentation.pubg.com/en/telemetry-events.html>`_

.. code-block:: python

    # Get all TelemetryEvents as a list
    events = telemetry.events

    # Get one of the events
    event = events[0]

    event.event_type
    # log_match_definition

    event.timestamp
    # '2019-08-18T00:29:00.0807375Z'

    event.to_dict()
    # {'_D': '2019-08-18T00:29:00.0807375Z', '_T': 'LogMatchDefinition', 'match_id': 'match.bro.official.pc-2018-04.steam.duo-fpp.na.2019.08.18.00.e0b3cb15-929f-4b42-8873-68a8f9998d2b', 'ping_quality': 'low', 'season_state': 'progress'}

    print(event.dumps())
    # {
    #     "_D": "2019-08-18T00:29:00.0807375Z",
    #     "_T": "LogMatchDefinition",
    #     "match_id": "match.bro.official.pc-2018-04.steam.duo-fpp.na.2019.08.18.00.e0b3cb15-929f-4b42-8873-68a8f9998d2b",
    #     "ping_quality": "low",
    #     "season_state": "progress"
    # }

    # Each event key can be grabbed as an attribute or key
    event.ping_quality
    # low

    event["ping_quality"]
    # low


TelemetryObjects refer to entities such as players, items, locations, vehicles, etc.
Each TelemetryObject contains a ``reference`` attribute which is the key in the parent
TelemetryEvent or TelemetryObject that refers to this TelemetryObject.

`Telemetry Objects <https://documentation.pubg.com/en/telemetry-objects.html>`_

.. code-block:: python

    # All available event types
    telemetry.event_types()
    # ['log_armor_destroy', 'log_care_package_land', 'log_care_package_spawn', 'log_game_state_periodic', 'log_heal'...

    kill_events = telemetry.filter_by("log_player_kill")
    kill = kill_events[0]

    kill.keys()
    # ['attack_id', 'killer', 'victim', 'assistant', 'dbno_id', 'damage_reason'...

    killer = kill.killer
    killer.keys()
    # ['reference', 'name', 'team_id', 'health', 'location', 'ranking', 'account_id', 'is_in_blue_zone', 'is_in_red_zone', 'zone']

    killer.name
    # 'WigglyPotato'

    victim = kill.victim
    victim.keys()
    # ['reference', 'name', 'team_id', 'health', 'location', 'ranking', 'account_id', 'is_in_blue_zone', 'is_in_red_zone', 'zone']

    victim.name
    # 'qnle'

    victim.to_dict()
    # {'account_id': 'account.d9c2d8dc8c03412eadfa3e59c8f3c16a', 'health': 0, 'is_in_blue_zone': False, 'is_in_red_zone': False...

    for k, v in victim.items():
        print(k, v)
    # reference victim
    # name qnle
    # team_id 43
    # health 0
    # location TelemetryObject location object
    # ranking 0
    # account_id account.d9c2d8dc8c03412eadfa3e59c8f3c16a
    # is_in_blue_zone False
    # is_in_red_zone False
    # zone ['georgopol']
