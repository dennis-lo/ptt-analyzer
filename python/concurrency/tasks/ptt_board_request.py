""" A class that represents a request to retrieve content from a PTT board """

from ..task import Task

class PttBoardRequest(Task):
    def __init__(self, board_name):
        super().__init__()
        self.board_name = board_name

