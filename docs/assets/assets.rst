Assets
======

Map Images
----------

Map images are sourced from an official PUBG repository
on github, `here <https://github.com/pubg/api-assets/tree/master/Assets/Maps>`__.

High resolution maps are not included in this package due to packaging size
limits on PyPI. You may download them manually and place them in the package's
folder: ``chicken_dinner/assets/maps`` in order to use them.

Alternatively you can download them using a function provided by the ``assets``
module. To download updated (and hi-res) maps directly from the official
PUBG assets GitHub project, run the following command from within your project
directory:

.. code-block:: bash

    python -m chicken_dinner.assets.maps

Starting in v0.10.0, they can also be downloaded using the chicken-dinner CLI:

.. code-block:: bash

    chicken-dinner assets

Asset Dictionary
----------------

There is an asset naming ``dictionary.json`` provided in the assets module that
is sourced from the official PUBG repository
on github, `here <https://github.com/pubg/api-assets/tree/master/dictionaries/telemetry>`_.

You can download an up-to-date version of the asset dictionary directly from
the GitHub source by running the following command from within your project
directory:

.. code-block:: bash

    python -m chicken_dinner.assets.dictionary

Starting in v0.10.0, they can also be downloaded using the chicken-dinner CLI:

.. code-block:: bash

    chicken-dinner assets

This mapping can be imported manually from the ``constants`` module using

.. code-block:: python

    from chicken_dinner.constants import asset_map

This asset dictionary can be used to map item/weapon/vehicle identifiers in
telemetry objects to their actual names. To do so automatically, pass the
``map_assets=True`` argument when creating a Telemetry instance.
