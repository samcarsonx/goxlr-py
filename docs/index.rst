.. mdinclude:: ../README.md
    :start-line: 0
    :end-line: 5

.. toctree::
    :maxdepth: 2
    :caption: Useful Links

    GitHub <https://github.com/samcarsonx/goxlr>
    PyPI <https://pypi.org/project/goxlr>
    Buy Me a Coffee <https://www.buymeacoffee.com/samcarsonx>

Features
--------

- Asynchronous connection to the GoXLR utility daemon
- All methods have been translated to Python
- Handy enumerators for everything
- Very simple and easy to get started

Installation
------------

.. code-block:: bash

    pip install goxlr

Getting Started
---------------

Here's some sample code to get started with this package that pings the utility's daemon.

.. literalinclude:: examples/gettingstarted.py
   :language: python
   :linenos:

You may have noticed that we use `with` to manage the connection to the GoXLR. You may also wish to use the more traditional open and close methods which is acceptable too.

.. literalinclude:: examples/gettingstarted2.py
   :language: python
   :linenos:

For detailed information on the API, refer to the following section:

.. toctree::
    :maxdepth: 2
    :caption: API Reference

    api/socket
    api/commands
    api/types
    api/error
    examples/index
