""" A class that represents a request to retrieve content from a PTT board """

import ptt.boards
from .http_request_task import HttpRequestTask


class PttBoardRequest(HttpRequestTask):

    def __init__(self, board_name: str, page_num: int = None):
        """ Instantiation

        Arguments:
            board_name -    Name of the board, e.g. "Baseball"
            page_num -      Index page number of the board
        """
        super().__init__(ptt.boards.get_url(board_name, page_num),
                         method='GET')
        self.board_name = board_name
