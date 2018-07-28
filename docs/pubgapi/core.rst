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

.. warning::

    *(new in 0.4.0)* PUBGCore (and PUBG) instances provide a built-in rate
    limiter which sleeps based on the API call being made and the rate limit
    information contained in the response headers. When rate limited, these
    classes will emit a warning to the console.

    PUBGCore will attempt to avoid 429 (rate limited) responses
    altogether, but if a 429 response does occur, the client will sleep and
    attempt *one* retry before raising an exception.


.. autoclass:: chicken_dinner.pubgapi.PUBGCore
    :members:
