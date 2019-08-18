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

Example

.. code-block:: bash

    $ chicken-dinner leaderboard solo-fpp

      rank  name                rank_points    wins    games    win_ratio    average_damage    kills    kill_death_ratio    average_rank
    ------  ----------------  -------------  ------  -------  -----------  ----------------  -------  ------------------  --------------
         1  HuYa-17152571              6344      82     1595    0.0514107               247     3229             2.12714         37.6796
         2  Huya_15007597_LS           6317     134     1240    0.108065                336     3643             3.28494         31.6234
         3  Douyu-7250640              6317      61     1831    0.0333151               312     4871             2.75198         42.8514
         4  Douyu-4778209              6314      85     1402    0.0606277               249     2978             2.25265         32.6098
         5  DouYu-1673291              6233      67     1331    0.0503381               181     2023             1.60047         33.0834
         6  DouYuTv_4872341            6197     134     1051    0.127498                268     2468             2.67389         25.5138
         7  twitch_tmathree            6121      90      739    0.121786                486     3039             4.68259         36.4073
         8  HuYaTv-19488958            6116      16     1536    0.0104167               134     1741             1.14539         50.3125
         9  Breukin224                 6107      31      992    0.03125                 322     2772             2.86068         51.8054
        10  Huya_19317807              6090      83      743    0.111709                414     2729             4.12859         33.611
        11  HUYA_ID19443099            6080      33     1211    0.0272502               204     2064             1.75212         39.052
        12  Shocki-                    6078      30      685    0.0437956               293     1592             2.43053         41.3445
        13  TheFlet_YOUTUBE            6075      56      942    0.059448                367     2985             3.36907         55.0881
        14  kdl139                     6068      27     1052    0.0256654               150     1206             1.16297         26.4582
        15  CCTV_JIAOZHUANG            6062      50      980    0.0510204               331     2784             2.99355         38.8153
        16  Pashaebashy7               6057      46      767    0.0599739               277     1767             2.44737         43.5776
        17  DouyuXiaoLuFei             6054      58      685    0.0846715               294     1611             2.56529         34.8569
        18  2sit                       6047      22      671    0.0327869               167      872             1.34361         40.0686
        19  Saariankooh                6029      34      465    0.0731183               250      785             1.82135         26.6882
        20  kingkong2152               6028      22      579    0.0379965               250     1076             1.93178         32
        21  twitch-MozartUSA           6016      40      441    0.090703                296     1075             2.6808          23.7166
        22  DEBO4KA_DAYH               6012      38      433    0.0877598               286     1011             2.55303         26.0046
        23  HuYa_19131081              6009      47      799    0.0588235               245     1745             2.32048         41.6909
        24  WH_WenJiuGeGe              6004      56      713    0.0785414               392     2256             3.42857         41.4109
        25  Terrorist_-                6001      23      428    0.0537383               265      935             2.30864         25.535


Player Stats
------------

Display player stats for lifetime or the current season (shard default is steam):

.. code-block:: bash

    # Get the lifteime stats for chocoTaco in solo-fpp
    chicken-dinner stats --shard=steam --lifetime --group=solo --perspective=fpp chocoTaco

    # Get the latest season stats for chocoTaco in solo-fpp
    chicken-dinner stats -g solo -p fpp chocoTaco

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

    # Generate a replay for the latest win of chocoTaco in specified path
    chicken-dinner replay --latest --wins-only --size=6 --path=/path/to/my/replays chocoTaco

    # Generate a replay for the latest game of chocoTaco
    chicken-dinner replay -l chocoTaco

    # Generate a replay for all of chocoTaco's wins in recent games
    chicken-dinner replay -w chocoTaco

    # Generate a replay for all of the recent games of chocoTaco
    chicken-dinner replay chocoTaco
