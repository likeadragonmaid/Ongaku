if __name__ == "__main__":
    import logging
    import tracemalloc

    from ongaku import ongaku, Ongaku

    tracemalloc.start()
    logging.basicConfig(level=logging.ERROR)
    try:
        ongaku.run(ongaku.boot())
    except KeyboardInterrupt:
        ongaku.run(ongaku.set_bio(bio=ongaku.original_bio))
        ongaku.run(ongaku.log(text="Ongaku stopped."))
        print("\nOngaku: Stopped")