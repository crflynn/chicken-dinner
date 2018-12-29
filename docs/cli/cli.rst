Command line interface (CLI)
============================

Starting in version 0.8.0, ``chicken-dinner`` provides a limited CLI for

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
