0.2.1: 2018-06-22
~~~~~~~~~~~~~~~~~

* Added Sanhok (Savage_Main) map

* Removed /matches and /telemetry API calls from the rate limiter per the API documentation

0.2.0: 2018-06-16
~~~~~~~~~~~~~~~~~

* Telemetry.player_positions() now only show up to the first recorded dead position

* Playback animations now show PvP damage events

* Changed Telemetry.player_positions() events to use timestamps rather than timeElapsed to be consistent with other events

* Bugfix for dead highlight players affecting other player's death markers

* Bugfix for player deaths showing late.

0.1.2: 2018-06-10
~~~~~~~~~~~~~~~~~

* Bugfix for Telemetry import in Match object

* Bufgix for TypeError on highlights and labels in animations

0.1.1: 2018-06-10
~~~~~~~~~~~~~~~~~

* Fixed incorrect link in PyPI metadata

0.1.0: 2018-05-23
~~~~~~~~~~~~~~~~~

* Initial release.

* Core package elements for interfacing with the PUBG API and its models

* PUBGCore, PUBG classes

* PUBG Meta models (players, seasons, matches, rosters, participants, telemetry)

* Official map images

* Customizable html5 match playback visualization using ffmpeg
