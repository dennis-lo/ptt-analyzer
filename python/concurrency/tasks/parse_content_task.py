""" A class that represents a task of parsing content of a certain format """

from ..task import Task


class ParseContentTask(Task):
    def __init__(self, data):
        """ Instantiation

        Arguments:
            data -  Content to be parsed
        """
        super().__init__()
        self.data = data
