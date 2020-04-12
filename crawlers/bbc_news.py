import cralwer
import requests
from bs4 import BeautifulSoup
from loguru import logger


class BBCNews(cralwer.Crawler):
    def __init__(self, processor):
        super().__init__()
        self.name = 'BBC News'
        self.description = 'This module will crawl BBC News homepage for the latest stories'
        self.version = '1.0'
        self.bbc_links = []
        self.processor = processor

    def parse(self, response):
        logger.info("Parsing BBC News homepage...")
        parser = BeautifulSoup(response.text, 'html.parser')

        for a in parser.find_all("a", {"class": "gs-c-promo-heading"}):
            if "http://" in a.attrs['href']:
                continue

            if "https://" in a.attrs['href']:
                continue

            if "/sport/" in a.attrs['href']:
                continue

            self.bbc_links.append("https://www.bbc.co.uk" + a.attrs['href'])

        self.bbc_links = set(self.bbc_links)

        for article in self.bbc_links:
            logger.info("Adding article to queue: " + article)
            self.queue_article(article)

    def queue_article(self, url):
        self.processor.add_article_to_queue(url)

    def launch(self):
        url = 'https://www.bbc.co.uk/news'
        response = requests.get(url)

        self.parse(response)

    def crawl(self):
        logger.info("BBC News module called...")
        self.launch()
        return None
