class Crawler(object):
    def __init__(self):
        self.name = 'UNKNOWN'
        self.targets = []
        self.description = 'UNKNOWN'
        self.version = '0.0.0'
        self.processor = None

    def process_article(self, url):
        raise NotImplementedError

    def crawl(self):
        raise NotImplementedError
