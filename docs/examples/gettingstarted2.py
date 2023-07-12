import asyncio

from goxlr import GoXLR


async def main():
    xlr = GoXLR()
    await xlr.open()

    ping = await xlr.ping()
    print(ping)  # Ok

    await xlr.close()


if __name__ == "__main__":
    asyncio.run(main())
