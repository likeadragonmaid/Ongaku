import logging

from .ongaku import loop_, ongaku, reset_bio

logging.basicConfig(level=logging.ERROR)


async def boot():
    # importlib.import_module("bot.plugins.commands")
    await loop_()


if __name__ == "__main__":
    try:
        ongaku.run(boot())
    except KeyboardInterrupt:
        ongaku.run(reset_bio())
        print("\nOngaku: Stopped")
