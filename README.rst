Turbot implementation
=============================


Installation
------------

.. code::

    python setup.py install


Usage
-----


.. code:: python

    >>> import turbot
    >>> t = turbot.Turbot()
    >>> t.answer("When was Bjarne Stroustrup born?")
    'Bjarne Stroustrup was born on the 1950-12-30'
    >>> t.answer("Is the sky blue?")
    'Yes, the sky is blue.'
