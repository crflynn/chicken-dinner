Command line interface (CLI)
============================

Starting in version 0.10.0, ``chicken-dinner`` provides a limited CLI for

* updating local assets
* retrieving player stats
* displaying leaderboards
* creating telemetry replays

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

Help
----

For terminal based help, use ``-h`` or ``--help`` with or without a command

.. code-block:: bash

    chicken-dinner -h
    # or
    chicken-dinner stats --help


Assets
------

To update local assets, including hi-res maps and asset dictionaries:

.. code-block:: bash

    chicken-dinner assets

Leaderboards
------------

Display the leaderboards for a game mode (shard default is steam):

.. code-block:: bash

    chicken-dinner leaderboard --shard=steam solo-fpp


Player Stats
------------

Display player stats for lifetime or the current season (shard default is steam):

.. code-block:: bash

    # Get the lifteime stats for shroud in solo-fpp
    chicken-dinner stats --shard=steam --lifetime --group=solo --perspective=fpp shroud

    # Get the latest season stats for shroud in solo-fpp
    chicken-dinner stats -g solo -p fpp shroud

Example

.. code-block:: bash

    $ chicken-dinner stats chocoTaco -p fpp

    stats                  duo-fpp    solo-fpp    squad-fpp
    ---------------------  ---------  ----------  -----------
    assists                259        38          12
    boosts                 804        498         48
    dbnos                  658        0           43
    daily_kills            7          18          63
    daily_wins             0          0           1
    damage_dealt           140338.81  95036.79    6803.76
    days                   19         19          2
    headshot_kills         342        324         12
    heals                  901        501         64
    kill_points            0          0           0
    kills                  1252       874         63
    longest_kill           531.4734   708.46      298.46796
    longest_time_survived  1893.243   1890.955    1750.131
    losses                 276        208         13
    max_kill_streaks       3          5           3
    most_survival_time     1893.243   1890.955    1750.131
    rank_points            4930.005   4174.5967   2302.7534
    rank_points_title      5-1        5-5         3-4
    revives                139        0           8
    ride_distance          439681.06  233850.77   26140.986
    road_kills             11         5           0
    round_most_kills       15         20          12
    rounds_played          313        227         14
    suicides               9          3           0
    swim_distance          622.386    373.03534   375.89685
    team_kills             10         3           0
    time_survived          226039.02  117699.73   12748.38
    top_10s                83         28          5
    vehicle_destroys       17         13          0
    walk_distance          360149.94  160033.28   19540.883
    weapons_acquired       1327       746         64
    weekly_kills           292        170         63
    weekly_wins            7          6           1
    win_points             0          0           0
    wins                   40         19          1


Replays
-------

Generate html5 replays for matches (shard default is steam):

.. code-block:: bash

    # Generate a replay for the latest win of shroud in specified path
    chicken-dinner replay --latest --wins-only --size=6 --path=/path/to/my/replays shroud

    # Generate a replay for the latest game of shroud
    chicken-dinner replay -l shroud

    # Generate a replay for all of shrouds wins in recent games
    chicken-dinner replay -w shroud

    # Generate a replay for all of the recent games of shroud
    chicken-dinner replay shroud
