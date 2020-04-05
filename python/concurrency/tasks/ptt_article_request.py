""" A class that represents a request to retrieve content from a PTT board """

import ptt.boards
from .http_request_task import HttpRequestTask


class PttArticleRequest(HttpRequestTask):

    def __init__(self, board_name: str, article_path: str):
        """ Instantiation

        Arguments:
            board_name -    Name of the board, e.g. "Baseball"
            article_path -  Relative path to the article
        """
        super().__init__(
            ptt.boards.get_url(board_name, article_path=article_path),
            method='GET')
        self.board_name = board_name
        self.article_path = article_path
