Turbot implementation
=============================


Installation
------------

.. code::

    pip install turbot


Usage
-----


.. code:: python

    >>> import turbot
    >>> d = turbot.Definition()
    >>> d.answer("When was Bjarne Stroustrup born?")
    'Bjarne Stroustrup was born on the 1950-12-30'

    >>> d = turbot.Dialog()
    >>> d.answer("Is the sky blue?")
    'Yes, the sky is blue.'
