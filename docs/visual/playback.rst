Playback Visualizations
=======================

The ``chicken_dinner`` package provides (for now) one configurable playback
animation via the ``create_playback_animation`` function or by calling directly
the ``playback_animation`` method from a Telemetry instance.

The playback animation function depends on external python
packages ``matplotlib`` and ``pillow``. To install ``chicken_dinner`` with
these extra dependencies, use

.. code-block:: bash

    pip install chicken-dinner[visual]

In order to use the playback animation you will need to install an
additional piece of software called ``ffmepg``. To install ``ffmpeg`` on Mac,
use brew:

.. code-block:: bash

    brew install ffmpeg

For other platforms, see `here <https://www.ffmpeg.org/download.html>`_

Here is some example code for creating a playback animation:

.. code-block:: python

    from chicken_dinner.pubgapi import PUBG


    api_key = "MY_API_KEY"
    pubg = PUBG(api_key, "pc-na")

    me = pubg.players_from_names("my_username")[0]
    last_match_id = me.match_ids[0]

    last_match = pubg.match(last_match_id)
    last_match_telemetry = last_match.get_telemetry()

    last_match_telemetry.playback_animation("last_match.html")

Alternately you can use the ``create_playback_animation()`` function.

.. code-block:: python

    from chicken_dinner.pubgapi import PUBG
    from chicken_dinner.visual.playback import create_playback_animation


    api_key = "MY_API_KEY"
    pubg = PUBG(api_key, "pc-na")

    me = pubg.players_from_names("my_username")[0]
    last_match_id = me.match_ids[0]

    last_match = pubg.match(last_match_id)
    last_match_telemetry = last_match.get_telemetry()

    create_playback_animation(last_match_telemetry, "last_match.html")


.. autofunction:: chicken_dinner.visual.playback.create_playback_animation
