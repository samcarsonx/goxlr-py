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

.. code-block:: python

    import asyncio

    from goxlr import GoXLR
    from goxlr.types import Fader, Channel

    async def main():
        async with GoXLR() as xlr:
            await xlr.set_fader(Fader.A, Channel.Headphones)
            await xlr.set_volume(Channel.Headphones, 0.5)

    if __name__ == "__main__":
        asyncio.run(main())

You may have noticed that we use `with` to manage the connection to the GoXLR. You may also wish to use the more traditional open and close methods which is acceptable too.

.. code-block:: python

    async def main():
        xlr = GoXLR()
        await xlr.open()

        ping = await xlr.ping()
        print(ping)  # Ok

        await xlr.close()

For detailed information on the API, refer to the following section:

.. toctree::
    :maxdepth: 2
    :caption: API Reference

    api/socket
    api/commands
    api/types
    api/error
