import pkgutil
import inspect
from loguru import logger
from cralwer import Crawler
from process import TaskQueue


class BellviewCore(object):

    def __init__(self, crawler_folder):
        logger.info("Loading crawlers...")

        self.crawler_folder = crawler_folder
        self.crawlers = []
        self.processor = TaskQueue()
        self.load_crawlers()
        self.list_crawlers()

    def load_crawlers(self):
        self.find_crawlers(self.crawler_folder)
        return True

    def list_crawlers(self):
        for crawler in self.crawlers:
            logger.info(
                f'Crawler name: {crawler.name} - Description: {crawler.description} - Version: {crawler.version}')
        return True

    def find_crawlers(self, folder):
        logger.info(f'Loading crawlers from: {folder}')
        imported_crawlers = __import__(folder, fromlist=['crawler'])
        for _, crawler_name, is_pkg in pkgutil.iter_modules(imported_crawlers.__path__, imported_crawlers.__name__ + '.'):
            if not is_pkg:
                crawler = __import__(crawler_name, fromlist=['crawler'])
                crawler_classes = inspect.getmembers(crawler, inspect.isclass)
                for (_, c) in crawler_classes:
                    if issubclass(c, Crawler) & (c is not Crawler):
                        self.crawlers.append(c(self.processor))
            else:
                logger.info("Not a crawler, skipping")

    def start(self):
        # TODO: Schedule each crawler to run on a defined interval
        for crawler in self.crawlers:
            try:
                crawler.crawl()
            except Exception as ex:
                if hasattr(ex, 'message'):
                    logger.error(ex.message)
                else:
                    logger.error(ex)
        logger.info("Articles in queue: ")
        logger.info(self.processor.get_queue_length())
        return True
