Release History
---------------

0.4.3: 2018-08-07
~~~~~~~~~~~~~~~~~

* Remove the unused game mode to game/perspective mappings from Match.game_mode attribute and PlayerSeason.game_mode_stats() method so that event modes (e.g. acpfpp) can be returned

0.4.2: 2018-07-30
~~~~~~~~~~~~~~~~~

* Fixed a bug in which rate limited headers should only be checked on responses to rate limited endpoints

0.4.1: 2018-07-28
~~~~~~~~~~~~~~~~~

* Fixed a bug that prevented the status method from returning because it is unauthenticated and has no limit headers

0.4.0: 2018-07-28
~~~~~~~~~~~~~~~~~

* Fixed a visual bug where dead highlighted labeled players' markers would persist after death
* Moved the map update module from visual to assets
* Added item id mapping dictionary in chicken_dinner/assets/dictionary.json
* Added item mapping dictionary update module in chicken_dinner.assets.dictionary
* Fixed chicken_dinner.__all__
* Added some missing imports
* Added optional ``map_assets`` boolean to Telemetry related builders/constructors which maps asset ids to asset names
* Removed the artificial rate limiter
* Added an internal rate limiter to PUBGCore based on response headers (timestamps and limit remaining)
* PUBGCore (and PUBG) now sleeps automatically for rate limited requests
* Rate limited sleeps now log at WARNING level
* PUBGCore now raises RequestException for all non-200 responses except with 429 where it will sleep and try once (and only once) more
* rate_limit_count and rate_limit_window parameters are now removed from the PUBG and PUBGCore classes as limits are now inferred from response headers

0.3.3: 2018-07-24
~~~~~~~~~~~~~~~~~

* Fix for missing import statement in telemetry.py
* Bugfix for blueZoneCustomOptions in TelemetryEvent.__init__()
* Bugfix for Telemetry.damage_done() and Telemetry.damage_taken() functions
* Allow events to be index-accessible in the Telemetry object

0.3.2: 2018-07-23
~~~~~~~~~~~~~~~~~

* Bugfix for overriding initial shard selection in PUBGCore (thanks to `CemuUser8 <https://github.com/CemuUser8>`_)

0.3.1: 2018-07-22
~~~~~~~~~~~~~~~~~

* Updates to the latest version of Miramar map image
* Provide a function for locally updating and downloading official PUBG map images, including hi-res versions

0.3.0: 2018-07-22
~~~~~~~~~~~~~~~~~

* Add support for tournament endpoints
* Provide Tournaments and Tournament objects
* Add better telemetry support with TelemetryEvent and TelemetryObject classes

0.2.7: 2018-07-20
~~~~~~~~~~~~~~~~~

* Remove a print statement in Telemetry.player_damage()

0.2.6: 2018-07-20
~~~~~~~~~~~~~~~~~

* Bugfix in Telemetry.player_damage() for damage events with attacker = None (knocked bleedout damage)
* Bugfix for visualizations with players that have no telemetry positions

0.2.5: 2018-07-02
~~~~~~~~~~~~~~~~~

* Bugfix for empty player position lists in telemetry

0.2.4: 2018-07-01
~~~~~~~~~~~~~~~~~

* Bugfix for second place player markers not disappearing

* Small fix to make Telemetry.killed() more reliable since API might not provide all killed events

0.2.3: 2018-07-01
~~~~~~~~~~~~~~~~~

* Added zordering to plot elements for better visualizations

0.2.2: 2018-06-30
~~~~~~~~~~~~~~~~~

* Deprecated player.attributes.createdAt and player.attributes.updatedAt per API v1.5.1

* Fixed map name access in telemetry methods due to changes in API v1.5.1

* Added map id method to telemetry

* Added package metadata access to package level

* Added is_custom method to match objects

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
