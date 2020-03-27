""" A worker that parses HTML content """

from ..worker import Worker

class HtmlContentParser(Worker):

    def handle_task(self, task):
        """ Handles task and returns results """
        return (False, None)

