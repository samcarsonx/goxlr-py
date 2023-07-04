# GoXLR Utility API Python Wrapper

 [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![PyPI version](https://badge.fury.io/py/goxlr.svg)](https://badge.fury.io/py/goxlr) ![PyPI - Downloads](https://img.shields.io/pypi/dm/goxlr) ![GitHub issues](https://img.shields.io/github/issues/samcarsonx/goxlr) [![Documentation Status](https://readthedocs.org/projects/goxlr/badge/?version=latest)](https://goxlr.readthedocs.io/en/latest/?badge=latest)

A python wrapper for the API of the open-source GoXLR software alternative, GoXLR Utility, that uses asyncio. Disclaimer: This project is not affiliated with the GoXLR brand or TC-Helicon in any way, shape, or form. This is a third-party package made for fun and educational purposes.

## Features
- Asynchronous connection to the GoXLR utility daemon
- Almost all methods have been translated to Python
- Handy enumerators for everything
- Very simple and easy to get started

## Installation
```shell
pip install goxlr
```

## Getting Started
Here's some sample code to get started with this package that pings the utility's daemon.
```py
import asyncio
from goxlr import GoXLR

async def main():
    async with GoXLR() as xlr:
        print(await xlr.ping())

if __name__ == "__main__":
    asyncio.run(main())
```
You may have noticed that we use `with` to manage the connection to the GoXLR. You may also wish to use the more traditional open and close methods which is acceptable too.
```py
async def main():
    xlr = GoXLR()
    xlr.connect()
    print(await xlr.ping())
    xlr.close()
```

## Contributing
Coming soon. As there isn't a CONTRIBUTING.md yet, please try to emulate the style of the rest of the code. Using snake_case and descriptive method argument names with type hints wherever possible.

## Documentation
Please visit the [documentation](https://goxlr.readthedocs.io/en/latest/) for more information on how to use this package.