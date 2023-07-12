import asyncio
import json
from goxlr import GoXLR
from goxlr.types import Channel, Fader, Button


with open("docs/examples/paging.json") as f:
    pages = json.load(f)


async def main():
    async with GoXLR() as goxlr:
        print("Connected to GoXLR")

        while True:
            page = goxlr.get_active_effect_preset().name.removeprefix("Preset")
            page = (int(page) - 1) % len(pages) + 1

            print(f"Page {page}")

            faders = pages[str(page)]

            for fader, data in faders.items():
                channel = getattr(Channel, data["channel"])

                await goxlr.set_fader(Fader[fader], channel)
                await goxlr.set_scribble_text(Fader[fader], channel.name)
                await goxlr.set_scribble_icon(Fader[fader], data["icon"])

            presets = [
                Button.EffectSelect1,
                Button.EffectSelect2,
                Button.EffectSelect3,
                Button.EffectSelect4,
                Button.EffectSelect5,
                Button.EffectSelect6,
            ]

            await goxlr.wait_for_button(presets)
            await goxlr.wait_for_button(presets, all_values=True, invert=True)


asyncio.run(main())
