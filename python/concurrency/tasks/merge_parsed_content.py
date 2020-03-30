""" A class that represents a task of merging parsed content """

from ..task import Task

class MergeParsedContent(Task):
    def __init__(self, data):
        """ Instantiation

        Arguments:
            data -  Content to be merged
        """
        super().__init__()
        self.data = data

