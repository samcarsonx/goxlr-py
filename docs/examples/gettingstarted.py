import asyncio

from goxlr import GoXLR
from goxlr.types import Fader, Channel


async def main():
    async with GoXLR() as xlr:
        await xlr.set_fader(Fader.A, Channel.Headphones)
        await xlr.set_volume(Channel.Headphones, 127)


if __name__ == "__main__":
    asyncio.run(main())
