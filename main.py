import asyncio
from goxlr import GoXLR
from goxlr.types import ChannelName


async def main():
    async with GoXLR() as xlr:
        await xlr.set_volume(ChannelName.Headphones, 127)


if __name__ == "__main__":
    asyncio.run(main())
