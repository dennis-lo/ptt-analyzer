""" A class that represents a task of parsing content of a certain format """

from .parse_content_task import ParseContentTask

class ParsePttBoardIndex(ParseContentTask):
    def __init__(self, data):
        """ Instantiation

        Arguments:
            data -  Content to be parsed
        """
        super().__init__(data)

