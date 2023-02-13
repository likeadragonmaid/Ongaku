import logging

from ongaku.looper import loop_, reset_bio

from ongaku import ongaku

logging.basicConfig(level=logging.ERROR)


async def boot():
    # importlib.import_module("bot.plugins.commands")
    await loop_()


if __name__ == "__main__":
    try:
        ongaku.start()
        ongaku.run(boot())
    except KeyboardInterrupt:
        ongaku.run(reset_bio(restart=False))
        print("\nOngaku: Stopped")
