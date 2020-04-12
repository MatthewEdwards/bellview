from loguru import logger
from bellview import BellviewCore


def main():
    logger.add("bellview.log")
    logger.info("Launching bellview...")
    bellview = BellviewCore('crawlers')
    bellview.start()


if __name__ == "__main__":
    main()
