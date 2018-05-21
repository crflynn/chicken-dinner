PUBG API Core
=============

The ``chicken_dinner`` package provides a core class for low-level interaction
with the PUBG JSON API. To use it, you will need an api key, which you can get
from the developer portal here: https://developer.playbattlegrounds.com/.

Each method provides a deserialized JSON response for each of the endpoints
provided by the API. Use this if you plan on working directly with the raw
JSON responses from the API.

To interact with the API on a higher level refer to the documentation for
the :class:`chicken_dinner.pubgapi.PUBG` class.

Developer api keys come with a rate limit of 10 API calls per 60 seconds. The
``PUBGCore`` class provides a (blocking) built-in rate limiter that sleeps
automatically between consecutive requests to prevent hitting the rate limit.
If you have an API key with a higher rate limit you can provide the parameters
on instantiating the ``PUBGCore`` class.

.. autoclass:: chicken_dinner.pubgapi.PUBGCore
    :members:
