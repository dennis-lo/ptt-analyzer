""" A worker that read content from a PTT board """

from ..worker import Worker

class PttBoardReader(Worker):

    def handle_task(self, task):
        """ Handles task and returns results """
        return (False, None)

