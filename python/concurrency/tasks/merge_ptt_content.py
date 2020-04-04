""" A class that represents a task of merging PTT content """

from .merge_parsed_content import MergeParsedContent


class MergePttContent(MergeParsedContent):
    def __init__(self, data):
        """ Instantiation

        Arguments:
            data -  Content to be merged
        """
        super().__init__(data)
