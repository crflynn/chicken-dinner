Map Images
==========

Map images are sourced from an official PUBG repository
on github, `here <https://github.com/pubg/api-assets/tree/master/Assets/Maps>`_.

High resolution maps are not included in this package due to packaging size
limits on PyPI. You may download them manually and place them in the package's
folder: ``chicken_dinner/assets/maps`` in order to use them.

Alternatively you can download them using a function provided by the ``visual``
module. To download updated (and hi-res) maps directly from the official
PUBG assets GitHub project, run the following command from within your project
directory:

.. code-block:: bash

    python -m chicken_dinner.visual.maps
