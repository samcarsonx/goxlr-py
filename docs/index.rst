.. mdinclude:: ../README.md
    :start-line: 0
    :end-line: 5

Features
--------

- Asynchronous connection to the GoXLR utility daemon
- Almost all methods have been translated to Python
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

    async def main():
        async with GoXLR() as xlr:
            print(await xlr.ping())

    asyncio.run(main())

You may have noticed that we use `with` to manage the connection to the GoXLR. You may also wish to use the more traditional open and close methods which is acceptable too.

.. code-block:: python

    import asyncio
    from goxlr import GoXLR

    async def main():
        xlr = GoXLR()
        await xlr.connect()
        print(await xlr.ping())
        await xlr.close()

    asyncio.run(main())


API Reference
-------------

For detailed information on the API, refer to the following section:

.. toctree::
    :maxdepth: 2

    api/ws
    api/goxlr
    api/error
    api/types
