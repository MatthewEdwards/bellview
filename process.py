import redis
from rq import Queue



class TaskQueue(object):

    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        self.q = Queue(connection=self.r)

    def get_queue_length(self):
        return len(self.q)

    def clear_queue(self):
        self.q.empty()

    def add_article_to_queue(self, url):
        result = self.q.enqueue(url)
        pass
